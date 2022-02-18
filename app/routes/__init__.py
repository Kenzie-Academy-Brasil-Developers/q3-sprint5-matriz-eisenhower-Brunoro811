from flask import Flask

from app.routes.categorys_route import bp as bp_category
from app.routes.tasks_route import bp as bp_tasks

def init_app(app:Flask):
    app.register_blueprint(bp_category)
    app.register_blueprint(bp_tasks)
