from flask import Blueprint, render_template, request, redirect, url_for, flash
from pokemon.extensions import db, bcrypt
from pokemon.models import User
from flask_login import login_user, logout_user, current_user, login_required
from pokemon.users.forms import ChangePasswordForm 

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/')
@login_required
def index():
    return render_template('users/index.html', title='User Page')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        query = db.select(User).where(User.username==username)
        user = db.session.scalar(query)
        if user:
            flash('Username is already exists!', 'warning')
            return redirect(url_for('users.register'))
        
        if password == confirm_password:
            pwd_hash = bcrypt.generate_password_hash(password=password).decode('utf-8')
            user = User(username=username, email=email, password=pwd_hash)
            db.session.add(user)
            db.session.commit()
            flash('Register successful!', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('Your password not match!', 'warning')
    return render_template('users/register.html', title='Register Page')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.session.scalar(db.select(User).where(User.username==username))
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('core.index'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('users/login.html', title='Login Page')

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users_bp.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Old password is incorrect.', 'danger')
    return render_template('users/change_password.html', title='Change Password', form=form)

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.firstname = request.form.get('firstname')
        current_user.lastname = request.form.get('lastname')
        db.session.commit()
        flash('Update profile successful!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('users/profile.html', title='Profile Page', user=current_user)