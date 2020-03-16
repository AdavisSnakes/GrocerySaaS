import time
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from cartdb import CartAccess

db_access = CartAccess()


class CartAction():
    def test(self):
        return
