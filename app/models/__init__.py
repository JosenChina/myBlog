from .Role import Role
from .User import User
from .Post import Post
from .Follow import Follow
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
