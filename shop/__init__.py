from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'sdfsdfsdwrt435342sdf'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)        # 16 megabytes

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# The following code is for getting rid of circular import
# Will modify later
if True:
    from shop.products import routes
    from shop.admin import routes
    from shop.carts import carts
