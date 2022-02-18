from flask import Blueprint

from app.controllers import categorys_controllers

bp = Blueprint("categories",__name__,url_prefix="/categories")

bp.post("")(categorys_controllers.create_category)
bp.get("")(categorys_controllers.get_categorys)
bp.get("<int:id>")(categorys_controllers.get_one_category)
bp.patch("<int:id>")(categorys_controllers.update_category)
bp.delete("<int:id>")(categorys_controllers.delete_category)