from flask import current_app, jsonify, request
from sqlalchemy.orm import Session
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from psycopg2.errors import UniqueViolation
from app.controllers.decorators import verify_types
from app.controllers.exc.category_exc import JSONNotFound

from app.models.category_model import CategoryModel

@verify_types({
	"name": str,
	"description": str
})
def create_category():
    try:
        session: Session = current_app.db.session
        if not request.get_json():
            raise JSONNotFound
        data = request.get_json()
        new_category = CategoryModel(**data)
        session.add(new_category)
        session.commit()

        return jsonify(new_category),HTTPStatus.CREATED
    except JSONNotFound as e:
        return {"error": "Body no have JSON"},HTTPStatus.UNPROCESSABLE_ENTITY
    except (UniqueViolation,IntegrityError):
        return { "msg": "category already exists!"},HTTPStatus.CONFLICT
    except Exception as e:
        raise e

def get_categorys():
    try:
        all_categorys = CategoryModel.query.all()

        return jsonify(all_categorys),HTTPStatus.OK
    except Exception as e:
        raise e

def get_one_category(id: int):
    try:
        category: CategoryModel = CategoryModel.query.get(id)
        if not category:
            raise NoResultFound
            
        return jsonify(category),HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not found category."},HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e

@verify_types({
	"name": str,
	"description": str
},opitional_keys=True)
def update_category(id: int):
    try:
        session: Session = current_app.db.session
        category = CategoryModel.query.get(id)
        if not category:
            raise NoResultFound
        
        if not request.get_json():
            raise JSONNotFound
        data: dict = request.get_json()

        for key,value in data.items():
            setattr(category,key,value)
        session.add(category)
        session.commit()
            
        return jsonify(category),HTTPStatus.OK
    except JSONNotFound as e:
        return {"error": "Body no have JSON"},HTTPStatus.UNPROCESSABLE_ENTITY
    except NoResultFound:
        return {"msg": "category not found!"},HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e


def delete_category(id: int):
    try:
        session: Session = current_app.db.session
        category = CategoryModel.query.get(id)
        if not category:
            raise NoResultFound
        session.delete(category)
        session.commit()
        
        return "",HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"msg": "category not found!"},HTTPStatus.NOT_FOUND
    except Exception as e:
        raise e