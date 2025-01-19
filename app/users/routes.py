from flask import render_template
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_security import roles_accepted
from app.users import bp
from app.extensions import db, bcrypt
from app.models.user import User, Role, get_user


@bp.route('/', methods=['GET'])
@roles_accepted('admin', 'supervisor')
def index():
    """ Display the list of users.

    Methods:
        GET: Retrieve and display all user records, ordered by user name.

    Returns:
        Template: Render the users/index.html template with user data.
    """
    users = User.query.order_by(User.user_name).all()
    return render_template('users/index.html', users=users)


@bp.route('/search_user/', methods=['GET', 'POST'])
@roles_accepted('admin', 'supervisor')
def search_user():
    """ Search for users based on a search string.

    Methods:
        GET/POST: Retrieve and display user records that match the search
        criteria.

    Returns:
        Template: Render the users/search_user.html template with
        search results.
    """
    search = request.args.get('search', '')
    users = get_user(search)
    return render_template('users/search_user.html', users=users)


@bp.route('/add_user/', methods=['POST', 'GET'])
@roles_accepted('admin')
def add_user():
    """ Add a new user.

    Methods:
        GET: Render the add user template.
        POST: Add a new user to the database.

    Returns:
        Template or redirect: Render the add user template or redirect
        to the users index.
    """
    if request.method == 'POST':
        user_name = request.form['user']
        user_email = request.form['user_email']
        user_phone = request.form['user_phone']
        password = request.form['user_password']
        user_role = request.form['privilege']

        hashed_password = bcrypt.generate_password_hash(password
                                                        ).decode('utf-8')
        role = Role.query.filter_by(name=user_role).first()
        new_user = User(user_name=user_name, user_email=user_email,
                        user_phone=user_phone, password=hashed_password)
        new_user.roles.append(role)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("users.index"))
        except:
            return 'There was an error adding user'
    else:
        return render_template('users/add_user.html')


@bp.route('/info_user/<int:id>', methods=['GET'])
@roles_accepted('admin', 'supervisor')
def info_user(id):
    """ Display information about a single user.

    Methods:
        GET: Retrieve and display information about a specific user.
    Returns:
        Template: Render the users/info_user.html template with user data.
    """
    user = User.query.get_or_404(id)
    return render_template('users/info_user.html', user=user)


@bp.route('/delete_user/<int:id>')
@roles_accepted('admin')
def delete_user(id):
    """ Delete a single user.

    Methods:
        GET: Delete a specific user from the database.

    Returns:
        Redirect: Redirect to the users index after deletion.
    """
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for("users.index"))
    except:
        return 'delete error'


@bp.route('/update_user/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin')
def update_user(id):
    """ Update information about a single user.

    Methods:
        GET: Render the update user template with the current user data.
        POST: Update the user information in the database.

    Returns:
        Template or redirect: Render the update user template or redirect
        to the users index.
    """
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.user_name = request.form['user']
        user.user_email = request.form['user_email']
        user.user_phone = request.form['user_phone']
        user.password = request.form['user_password']
        user.type = request.form['privilege']

        try:
            db.session.commit()
            return redirect(url_for("users.index"))
        except:
            return 'db update error'

    else:
        return render_template('users/update_user.html', user=user)
