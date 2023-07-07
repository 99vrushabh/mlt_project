from common.models import Signup
from tenants.admin.api import session
from common.database import switch_tenant
from tenants.user.service import authenticate, comments, details_user, signup_user
from flask_login import login_required, login_user, logout_user
from flask import Blueprint, redirect, render_template, request, url_for , g

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
        user = authenticate()
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
    user=details_user()
    return render_template('profile.html',name=user.name,email=user.email,phone=user.phone)

@user_api.route("/comment/<string:tenant>", methods=['GET', 'POST'])
@login_required
@switch_tenant
def comment(tenant):
    if tenant:
        if request.method == 'POST':
            new_comment= comments(tenant)
            if new_comment is not None:
                session.add(new_comment)
                session.commit()
                session.close()
                return redirect(url_for('store_page.store_home', tenant=tenant))
            else:
                session.close()
                return "not post"

    else:
        return "There is no store."

    return render_template('store/home.html', schema=g.tenant)


@user_api.route('/logout')
@login_required
def logout():   
    logout_user()
    Signup.is_active=False
    return redirect('login')