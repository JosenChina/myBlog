# _*_ coding : utf-8 _*_
# filename : __init.py

from flask import Blueprint
_main = Blueprint('main', __name__)

from .view import *
from .errors import *
from app.models.Role import Permission


@_main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
