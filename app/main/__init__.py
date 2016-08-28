from flask import Blueprint
from ..models import Permissions

main = Blueprint('main', __name__)

from . import views


@main.app_context_processor
def inject_permissions():
    return dict(Permissions=Permissions)
