import os
import stripe
from flask import request

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

# Import all the things
from setup_app import app
from cart_action import CartAction

action = CartAction(app)