from flask import Blueprint, redirect, render_template, request, url_for , g,jsonify
from flask_login import current_user, login_required, login_user, logout_user
import jwt
from common.database import db, switch_tenant
from common.models import Signup, new_store
from common.service import change_tenant
from tenants.user.service import authenticate, comment_user, signup_user

user_api = Blueprint('user_api',__name__,template_folder='templates',static_folder='static')


@user_api.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = signup_user()
        return redirect(url_for('user_api.login'))
    return render_template("form.html")

@user_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = authenticate(email, password)
        if user:
            login_user(user)
            return redirect(url_for('admin_page.admin_home', user_id=user.id))
        else:
            msg = 'Username or Password is wrong'
            return render_template('form.html', msg=msg)
    return render_template('form.html')

@user_api.route("/profile")
@login_required
def profile():
    user=current_user
    return render_template('profile.html',name=user.name,email=user.email,phone=user.phone)

@user_api.route("/comment/<string:tenant>", methods=['POST'])
@login_required
@switch_tenant
def comment(tenant):
    schema_name = new_store
    change_tenant(schema_name)
    if request.method == 'POST':
        comment_title = request.form.get("title")
        comment_desc = request.form.get("desc")
        comment_by = str(current_user.email)
        comment = comment_user(comment_title, comment_desc, comment_by)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment added successfully'})
    return render_template('store/home.html')

@user_api.route('/logout')
@login_required
def logout():   
    logout_user()
    Signup.is_active=False
    return redirect('login')