
class Warning(BaseException):
    pass
    
class ValidationError(BaseException):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
        
    def __unicode__(self):
        return self.message
