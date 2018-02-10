# _*_ coding:utf-8 _*_
# filename:form.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email
from wtforms import ValidationError
from ...models import User, Role


class AdminEditUserCenterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='此处不能为空！'),
                        Length(1, 64, message='长度不能超过64！'), Email('请输入正确的邮箱格式！')])
    username = StringField('用户名', validators=[DataRequired('此处不能为空！'),\
                           Length(0, 64, message='长度不能超过64位'),\
                           Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0, '请输入英文字母开头且不含数字、字母、下划线以外的字符')])
    confirmed = BooleanField('邮箱是否验证')
    role = SelectField('角色', coerce=int)
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('个性签名')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(AdminEditUserCenterForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and\
                User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册！')

    def validate_username(self, field):
        if field.data != self.user.username and\
                User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册！')
