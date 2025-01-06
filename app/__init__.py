from flask import Flask
from config import Config
from app.extensions import db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_security import Security, SQLAlchemySessionUserDatastore


bcrypt = Bcrypt() 
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from app.models.user import User, Role, create_roles
    create_roles()
    datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, datastore)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.sales import bp as sales_bp
    app.register_blueprint(sales_bp, url_prefix='/sales')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.customers import bp as customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')

    return app
