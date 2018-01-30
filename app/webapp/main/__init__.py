# _*_ coding : utf-8 _*_
# filename : __init.py

from flask import Blueprint
main = Blueprint('main', __name__)

from .login import *
