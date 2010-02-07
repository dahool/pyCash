import datetime

def remainInstalments(dateStart, dateEnd, pays):
    if dateStart>dateEnd:
        return pays
    
    delta = dateEnd - dateStart
    diff = (delta / 30).days
    if diff>pays:
        return 0
    
    return pays - diff

def test():

    tests=[]
    tests.append({'start': datetime.date(2008,11,8), 'end': datetime.date(2009,11,8), 'pays': 24, 'res': 12})
    tests.append({'start': datetime.date(2008,11,8), 'end': datetime.date(2009,8,25), 'pays': 24, 'res': 15})
    tests.append({'start': datetime.date(2008,2,2), 'end': datetime.date(2009,8,25), 'pays': 3, 'res': 0})
    tests.append({'start': datetime.date(2008,2,2), 'end': datetime.date(2008,3,25), 'pays': 3, 'res': 2})
    tests.append({'start': datetime.date(2008,2,2), 'end': datetime.date(2008,2,1), 'pays': 3, 'res': 3})
    tests.append({'start': datetime.date(2008,2,2), 'end': datetime.date(2008,3,25), 'pays': 1, 'res': 0})
    tests.append({'start': datetime.date(2008,2,2), 'end': datetime.date(2008,2,25), 'pays': 1, 'res': 1})
    
    for t in tests:
        r = remainInstalments(t.get('start'), t.get('end'), t.get('pays'))
        if t.get('res') == r:
            print "OK (%s, %s, %s, %s) => %s" % (t.get('start'), t.get('end'), t.get('pays'), t.get('res'), r)
        else:
            print "FAILED!! (%s, %s, %s, %s) => %s" % (t.get('start'), t.get('end'), t.get('pays'), t.get('res'), r)