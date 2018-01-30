# _*_ coding:utf-8 _*_
# filename:__init__.py
from flask import Blueprint
author = Blueprint('author', __name__)

from .post import *
