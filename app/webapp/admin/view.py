# _*_ coding:utf-8 _*_
# filename:view.py
from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from . import _admin
from app.decorators import admin_required
from app import db
from ...models import User, Role
from .form import AdminEditUserCenterForm


@_admin.route('/editCenter/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user_center(id):
    user = User.query.get_or_404(id)
    form = AdminEditUserCenterForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('用户资料已被更改！')
        return redirect(url_for('_user.user_center', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('admin/editUserCenter.html', form=form, user=user)


