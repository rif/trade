# -*- coding: utf-8 -*-

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth, Service, PluginManager, Crud

auth = Auth(db)
service = Service()
plugins = PluginManager()
crud = Crud(db)

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

"""
'order_id',
'portfolio_name',
'instrument_id',
'instrument_name',
'amount',
'broker_name',
'broker_id',
'broker_group_id',
'exchange',
'asset_class',
'order_type',
'price_limit',
'order_side',
'tag_name',
'tag_id',
'pre_trade_status',
'compliance_override_by',
'compliance_override_id',
'compliance_override_datetime',
'compliance_override_status',
'ipo_otc_flag',
'order_authorised_id',
'order_authorised_datetime',
'dealer_id',
'dealer_received_datetime',
'dealer_placed_datetime',
'commission_rate',
'commission_amount',
'confirmation_received_flag',
'confirmed_flag',
'confirmation_failure_flag',
'reconciled_flag',
'reconciled_datetime',
'instructed_flag',
'instructed_datetime',
'illiquid_flag',
'illiquid_pricing_source',
"""
Order = db.define_table('order',
                        Field('name'),
                        Field('amount', 'double'),
                        Field('compliant', 'boolean', default=False, readable=False, writable=False),
                        auth.signature
)

Portofolio = db.define_table('portofolio',
                        Field('agent', 'reference auth_user'),
                        Field('total', 'double'),
                        Field('average', 'double'),
                        Field('last_amount', 'double'),
                        Field('orders_count', 'integer'),
                        auth.signature
)

PortofolioRule = db.define_table('portofolio_rule',
                        Field('name'),
                        Field('code', 'text'),
                        auth.signature
)

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

a0, a1 = request.args(0), request.args(1)

# Populate some tables so we have data with which to work.
if db(db.auth_user).isempty():
    import datetime
    from gluon.contrib.populate import populate
    rif_id = db.auth_user.insert(first_name="Radu",last_name='Fericean',
                                 email='fericean@gmail.com',
                                 password=CRYPT()('test')[0])

    db.auth_membership.insert(user_id=rif_id, group_id=teacher_group_id())
    db.auth_membership.insert(user_id=rif_id, group_id=student_group_id())
                              
