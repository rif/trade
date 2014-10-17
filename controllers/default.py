# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from order_checker import order_checker

def index():
    form = SQLFORM(Order)
    if form.process().accepted:
        order = Order(form.vars.id)
        portofolio = db(Portofolio.agent==order.created_by).select().first()
        check = order_checker(form.vars,
                         portofolio,
                         db(PortofolioRule).select())
        if check[0]:
            # mark as compliant
            order.update_record(compliant=True)
            # update portofolio
            if not portofolio:
                Portofolio.insert(agent=order.created_by,
                                  total = order.amount,
                                  average = order.amount,
                                  last_amount = order.amount,
                                  orders_count = 1
                )
            else:
                portofolio.update_record(
                    total = portofolio.total + order.amount,
                    average = (portofolio.total + order.amount) / (portofolio.orders_count + 1),
                    last_amount = order.amount,
                    orders_count = portofolio.orders_count + 1
                )
            #redirect
            session.flash = 'order inserted'
            redirect('good_boy')
        else:
            session.flash = check[1]
            redirect('bad_boy')
    return dict(form=form)

def good_boy():
    response.view = 'default/redirect.html'
    return dict(title='Success!')

def bad_boy():
    response.view = 'default/redirect.html'
    return dict(title='Fail')

def rules():
    grid = SQLFORM.grid(PortofolioRule)
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
