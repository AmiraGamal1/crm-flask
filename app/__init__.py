from flask import Flask
from config import Config
from app.extensions import db
from flask_security import Security, SQLAlchemySessionUserDatastore
from app.extensions import login_manager, bcrypt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'amira'
    UPLOAD_FOLDER = 'uploads/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    
    from app.models.user import User, Role, create_roles
    create_roles()
    datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, datastore)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/main')

    from app.sales import bp as sales_bp
    app.register_blueprint(sales_bp, url_prefix='/sales')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.customers import bp as customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
