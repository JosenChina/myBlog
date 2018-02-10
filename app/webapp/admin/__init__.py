# _*_coding: utf-8 _*_
# filename: __init__py
from flask import Blueprint

_admin = Blueprint('admin', __name__)

from .view import *