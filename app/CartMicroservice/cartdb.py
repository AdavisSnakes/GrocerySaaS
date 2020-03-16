import json
from sqlalchemy.exc import IntegrityError
import traceback

from cart import db, Cart

class CartAccess():
    def __init__(self):
        self.db = db
        self.Cart = Cart

    def get_cart(self, user_id=None):
        return

    def add(self, user_id=None, cart_dict=None):
        return

    def remove(self, user_id=None, item=None, qty=None):
        return





