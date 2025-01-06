from flask import render_template
from flask import Flask, render_template, url_for, request, redirect
from flask_login import login_user, logout_user, login_required
from flask_security import Security, SQLAlchemySessionUserDatastore, roles_accepted
from app.users import bp
from app import bcrypt, login_manager
from app.extensions import db


from app.models.user import User, Role, get_user, create_roles


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@bp.route('/', methods=['GET', 'POST'])
def  login():
  if request.method == 'POST':
    user_email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(user_email=user_email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect('users/view_sale')
    else:
        return "login error"
  return render_template('users/login.html')

@bp.route('/logout')
@login_required
def  logout():
    logout_user()
    return redirect('/')

@bp.route('/view_user/', methods=['GET'])
@roles_accepted('admin', 'supervisor')
def view_user():
    """view user table"""
    users = User.query.order_by(User.user_name).all()
    return render_template('users/view_user.html', users=users)

@bp.route('/search_user/', methods=['GET', 'POST'])
@roles_accepted('admin','supervisor')
def search_user():
    search = request.args.get('search', '')
    users = get_user(search)
    return render_template('users/search_user.html', users=users)

@bp.route('/add_user/', methods=['POST', 'GET'])
@roles_accepted('admin')
def add_user():
    """add user"""
    if request.method == 'POST':
        user_name = request.form['user']
        user_email = request.form['user_email']
        user_phone = request.form['user_phone']
        password = request.form['user_password']
        user_role = request.form['privilege']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        role = Role.query.filter_by(name=user_role).first()
        new_user = User(user_name=user_name, user_email=user_email,
                        user_phone=user_phone, password=hashed_password)
        new_user.roles.append(role)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('users/view_user')
        except:
            return 'There was an error adding user'
    else:
        return render_template('users/add_user.html')

@bp.route('/info_user/<int:id>', methods=['GET'])
@roles_accepted('admin', 'supervisor')
def info_user(id):
    """info single user information"""
    user = User.query.get_or_404(id)
    return render_template('users/info_user.html', user=user)

@bp.route('/delete_user/<int:id>')
@roles_accepted('admin')
def delete_user(id):
    """delete single user"""
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('users/view_user')
    except:
        return 'delete error'

@bp.route('/update_user/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin')
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.user_name = request.form['user']
        user.user_email = request.form['user_email']
        user.user_phone = request.form['user_phone']
        user.password = request.form['user_password']
        user.type = request.form['privilege']

        try:
            db.session.commit()
            return redirect('users/view_user')
        except:
            return 'db update error'

    else:
        return render_template('users/update_user.html', user=user)
