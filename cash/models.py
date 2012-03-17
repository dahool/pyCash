from django.db import models
from cash.services.ModelUtils import capFirst

class Income(models.Model):
    period = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    
    def __unicode__(self):
        return self.period  
    class Meta:
        db_table = "income"
            
class PaymentType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def save(self):
        self.name = capFirst(self.name)
        super(PaymentType, self).save()
    def __unicode__(self):
        return self.name  
    class Meta:
        db_table = "payment_type"

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def save(self):
        self.name = capFirst(self.name)
        super(Category, self).save()
        
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = "category"

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", db_column="category_id")

    def save(self):
        self.name = capFirst(self.name)
        super(SubCategory, self).save()
            
    def __unicode__(self):
        return "%s - %s" % (self.name, self.category.name)  
    class Meta:
        db_table = "sub_category"
            
class Tax(models.Model):
    paymentType = models.ForeignKey(PaymentType,db_column="payment_type_id")
    subCategory = models.ForeignKey(SubCategory,db_column="sub_category_id")
    service = models.CharField(max_length=200, blank=False, unique=True)
    account = models.CharField(max_length=50, blank=True)
    expire = models.DateField(db_index=True,)
    nextExpire = models.DateField(null=True,db_column="next_expire")
    lastPay = models.DateField(null=True,db_column="last_pay")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    gcalId = models.CharField(max_length=50, blank=True, db_column="gcal_id")
    updated = models.BooleanField(default=False)
    
    def save(self):
        self.name = capFirst(self.service)
        super(Tax, self).save()
            
    def __unicode__(self):
        return self.service
    
    class Meta:
        db_table = "tax"
        
class Expense(models.Model):
    subCategory = models.ForeignKey(SubCategory, db_column="sub_category_id")
    paymentType = models.ForeignKey(PaymentType, db_column="payment_type_id")
    date = models.DateField(db_index=True)
    text = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    def save(self, **kwargs):
        self.name = capFirst(self.text)
        super(Expense, self).save(kwargs)
        
    def __unicode__(self):
        return "(%s) %s - %s" % (self.date, self.text, self.subCategory.name)

    class Meta:
        db_table = "expense"
        
class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def save(self):
        self.name = capFirst(self.name)
        super(Person, self).save()
            
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = "person"

class LoanManager(models.Manager):
    
    def active(self):
        return self.filter(remain__gt=0) 
    
    def fullpaid(self):
        return self.filter(remain=0)
    
class Loan(models.Model):
    person = models.ForeignKey(Person, db_column="person_id", related_name="loans")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateField(db_index=True)
    reason = models.CharField(max_length=255)
    instalments = models.IntegerField()
    remain = models.DecimalField(max_digits=19, decimal_places=2, db_index=True)
    
    objects = LoanManager()
    
    def save(self):
        self.name = capFirst(self.reason)
        super(Loan, self).save()
            
    def __unicode__(self):
        return "(%s) %s - %s" % (self.reason, self.amount, self.person.name)
    
    class Meta:
        db_table = "loan"
        
class Payment(models.Model):
    loan = models.ForeignKey(Loan, db_column="loan_id")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateField(db_index=True)
    
    def __unicode__(self):
        return "(%s) %s %s" % (self.loan.reason, self.amount, self.date)
    
    class Meta:
        db_table = "payment"
        ordering = ("-date",)
        
class Card(models.Model):
    name = models.CharField(max_length=50, unique=True)
    paymentType = models.ForeignKey(PaymentType, db_column="paymentType_id") 
    
    class Meta:
        db_table = "card"
        
class CardDates(models.Model):
    closeDate = models.DateField()
    expireDate = models.DateField()
    card = models.ForeignKey(Card, db_column="card_id")
    
    class Meta:
        db_table = "card_dates"
   
class CardData(models.Model):
    date = models.DateField()
    shop = models.CharField(max_length=100)
    instalments = models.IntegerField()
    total = models.DecimalField(max_digits=19, decimal_places=2)
    own = models.BooleanField()
    card = models.ForeignKey(Card, db_column="card_id")
    
    class Meta:
        db_table = "card_data"
         
class CardPayment(models.Model):
    minimum = models.DecimalField(max_digits=19, decimal_places=2)
    total = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.ForeignKey(CardDates, db_column="card_date_id")
    tax = models.ForeignKey(Tax, db_column="tax_id")
    
    class Meta:
        db_table = "card_payment"

class Debits(models.Model):
    day = models.IntegerField()
    subCategory = models.ForeignKey(SubCategory, db_column="sub_category_id")
    paymentType = models.ForeignKey(PaymentType, db_column="payment_type_id")
    text = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    since = models.DateField()
    last = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.text
        
    class Meta:
        db_table = "debits"
    
