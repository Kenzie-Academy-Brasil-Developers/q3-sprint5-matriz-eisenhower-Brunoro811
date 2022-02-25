from flask import Blueprint

from app.controllers import tasks_controllers


bp = Blueprint("all", __name__,url_prefix="/")

bp.get("")(tasks_controllers.get_tasks)