# _*_ coding: utf-8 _*_
# filename: view.py
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from . import _user
from app import db
from ...models import User
from .forms import LoginForm, RegisterForm, EditUserCenterForm
from ...mail import send_email


@_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        uu = User.query.filter_by(email=form.email.data).first()
        if uu is not None and uu.verify_password(form.password.data):
            login_user(uu, form.remember_me.data)
            flash('登录成功！')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('邮箱或密码错误！')
    return render_template('user/login.html', form=form)


@_user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录！')
    return redirect(url_for('main.index'))


@_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        uu = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(uu)
        db.session.commit()
        token = uu.generate_confirmation_token()
        send_email(uu.email, '确认账户邮箱！', 'user/email/confirm', uu=uu, token=token)
        flash('确认邮件已发送到您的邮箱，请注意查收！')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@_user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('激活成功！')
    else:
        flash('该激活链接已失效！')
    return redirect(url_for('main.index'))


@_user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed\
            and request.endpoint[:5] != 'user.' \
                and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@_user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/unconfirmed.html')


@_user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认账户邮箱', 'user/email/confirm', uu=current_user, token=token)
    flash('新的邮件已发送')
    return redirect(url_for('main.index'))


@_user.route('/userCenter/<username>')
def user_center(username):
    uu = User.query.filter_by(username=username).first()
    if uu is None:
        abort(404)
    return render_template('user/userCenter.html', user=uu)


@_user.route('/editUserCenter', methods=['GET', 'POST'])
def edit_user_center():
    form = EditUserCenterForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('更新成功！')
        return redirect(url_for('.user_center', username=current_user.username))
    form.name.data = current_user.name
    form.name.location = current_user.location
    form.name.about_me = current_user.about_me
    return render_template('editUserCenter.html', form=form)


