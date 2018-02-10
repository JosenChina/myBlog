# _*_ coding: utf-8 _*_
# filename: forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ...models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='请输入邮箱地址'),\
                                             Length(1, 64, message='邮箱地址长度不能超过64位'),\
                                             Email(message='请输入正确的邮箱地址')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='请输入邮箱！'), Length(1, 64, message='长度不能超过64位！'),\
                                             Email(message='邮箱格式输入有误！')])
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'), Length(6, 64, message='请输入6~64位用户名！'),\
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '首字符以英文字母开头，且不要输入字母、数字、下划线意外的字符')
    ])
    name = StringField('姓名', validators=[DataRequired(message='请输入个人姓名！')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码！')])
    password2 = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码输入不一致！')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册！')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('有用户名已存在！')


class EditUserCenterForm(FlaskForm):
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('个性签名')
    submit = SubmitField('提交')



