from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.eisenhowers_model import EisenhowerModel
    from app.models.category_model import CategoryModel
    from app.models.tasks_categorys_model import TasksCategoryModel
    from app.models.tasks_model import TasksModel