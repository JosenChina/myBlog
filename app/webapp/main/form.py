# _*_ coding: utf-8 _*_
# filename: form.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    body = PageDownField('博客内容', validators=[DataRequired('内容不能为空！')])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = TextAreaField('我来评论：', validators=[DataRequired('内容不能为空！')])
    submit = SubmitField('提交')

