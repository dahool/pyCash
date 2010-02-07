
def param_exist(var, req):
    return (var in req and req[var]!="")

def sortMethod(req):
    sort = req['sort']
    if param_exist("dir",req) and req['dir'].upper()=="DESC":
        sort = "-"+sort
    return sort