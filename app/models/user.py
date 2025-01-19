"""user modules to create table"""
from app.extensions import db
from datetime import datetime
import pytz
from flask_security import UserMixin, RoleMixin
import uuid
import secrets
from sqlalchemy.orm import aliased


fs_uniquifier_value = str(uuid.uuid4())


def generate_unique_value():
    """Generate a secure, unique value for the fs_uniquifier.
    """
    return secrets.token_urlsafe(16)


class User(db.Model, UserMixin):
    """User model representing the 'user' table in the database.

    Attributes:
        id (Integer): Primary key, unique identifier for each user.
        user_name (String): The name of the user.
        user_email (String): The email address of the user.
        user_phone (String): The phone number of the user.
        password (String): The hashed password of the user.
        active (Boolean): Indicates if the user is active.
        roles (Relationship): Relationship to the Role model,
        representing the user's roles.
        date (DateTime): The date when the user record was created.
        fs_uniquifier (String): A unique identifier for Flask-Security.

    Methods:
        __repr__(): Returns a string representation of the user object.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(200), nullable=False)
    user_phone = db.Column(db.String(15))
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary='user_roles',
                            backref='roled')
    date = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    fs_uniquifier = db.Column(db.String(90), nullable=False,
                              unique=True,
                              default=generate_unique_value)

    def __repr__(self):
        """Returns a string representation of the user object.

        Returns:
            str: A string that includes the user's name.
        """
        return f'<User "{self.user_name}">'


class Role(db.Model, RoleMixin):
    """Role model representing the 'role' table in the database.

    Attributes:
        id (Integer): Primary key, unique identifier for each role.
        name (String): The name of the role.

    Methods:
        __repr__(): Returns a string representation of the role object.
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        """Returns a string representation of the role object.
        Returns:
            str: A string that includes the role's name.
        """
        return f'<User "{self.name}">'


class UserRoles(db.Model):
    """UserRoles model representing the 'user_roles'
    table in the database,
    mapping users to their roles.

    Attributes:
        id (Integer): Primary key, unique identifier for each mapping.
        user_id (Integer): Foreign key to the user ID.
        role_id (Integer): Foreign key to the role ID.
    """
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
                                                  ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id',
                                                  ondelete='CASCADE'))


def create_roles():
    """Create default roles and add them to the database."""
    admin = Role(name='admin')
    editor = Role(name='editor')
    supervisor = Role(name='supervisor')
    try:
        db.session.add(admin)
        db.session.add(editor)
        db.session.add(supervisor)
        db.session.commit()
    except:
        return "fail to add roles to database"


def get_user(search):
    """Searches for users in the database using a search pattern.

    Parameters:
        search (str): The search string to look for in user records.

    Returns:
        list: A list of user objects matching the search criteria.
    """
    search_pattern = f"%{search}"
    RoleAlias = aliased(Role)
    results = User.query.filter(
        (User.id.like(search_pattern))
        | (User.user_name.like(search_pattern))
        | (User.user_email.like(search_pattern))
        | (User.user_phone.like(search_pattern))
        | (RoleAlias.name.like(search_pattern))
        | (User.date.like(search_pattern))
    ).all()
    return results
