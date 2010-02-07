
def capFirst(s):
    if len(s)>1:
        b = s[0].upper() + s[1:]
    else:
        b = s.upper()
    return b