
def param_exist(var, req):
    return (var in req and req[var]!="")

def sortMethod(req, value = None):
    if (value):
        sort = value
    else:
        sort = req['sort']
    if param_exist("dir",req) and req['dir'].upper()=="DESC":
        sort = "-"+sort
    return sort
