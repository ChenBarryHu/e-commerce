from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from flask_msearch import Search
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'sdfsdfsdwrt435342sdf'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)        # 16 megabytes

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please login first"


# Import these modules at the bottom to avoid circular import
if True:
    from shop.products import routes
    from shop.admin.routes import mgmt_bp
    from shop.carts import carts
    from shop.customers import routes
    app.register_blueprint(mgmt_bp)
