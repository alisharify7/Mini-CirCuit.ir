from Auth.Access.decorator import admin_login_required
from .model import Admin
from Core.extensions import db

def get_admin(id:int) -> Admin:
    """load -> return admin object base in primary key"""
    return db.session.get(Admin, id)