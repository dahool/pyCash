import datetime
import time
import calendar
from dateutil.relativedelta import relativedelta

# return the full date
def lastDateOfMonth(date):
    return datetime.date(date.tm_year, date.tm_mon, 
                             calendar.monthrange(date.tm_year,date.tm_mon)[1])   
# return the full date
def firstDateOfMonth(date):
    return datetime.date(date.tm_year, date.tm_mon, 1) 
    
def parse(str):
    return time.strptime(str,"%d/%m/%Y")

def invert(date):
    if isinstance(date,basestring):
        date = parse(date)
    elif isinstance(date,datetime.date):
        date = date.timetuple()
        
    return time.strftime("%Y-%m-%d",date)

def format(date):
    if isinstance(date,datetime.date):
        return time.strftime("%d/%m/%Y",date.timetuple())
    else:
        return time.strftime("%d/%m/%Y",date)

def midNight(date):
    if isinstance(date,datetime.date):
        dt = date.timetuple()
    else:
        dt = date
    return datetime.datetime(dt.tm_year, dt.tm_mon, dt.tm_mday, 0, 0,0)
    
def today():
    return time.localtime()

def todayDate():
    dt = time.localtime()
    return datetime.date(dt.tm_year, dt.tm_mon, dt.tm_mday)

def lastDayOfMonth(date):
    return calendar.monthrange(date.tm_year, date.tm_mon)[1]

def toLong(date):
    return int(time.mktime(date.timetuple())*1000)

def addMonth(date,n):
    delta = relativedelta(months=n)
    return date + delta