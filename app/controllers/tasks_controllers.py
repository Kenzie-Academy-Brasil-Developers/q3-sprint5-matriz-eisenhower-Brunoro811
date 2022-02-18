from flask import current_app, jsonify, request
from http import HTTPStatus
from app.controllers.decorators import verify_types

from app.controllers.exc.category_exc import JSONNotFound, ValueOutRange
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from psycopg2.errors import UniqueViolation

from app.models.category_model import CategoryModel
from app.models.eisenhowers_model import EisenhowerModel
from app.models.tasks_categorys_model import TasksCategoryModel
from app.models.tasks_model import TasksModel

@verify_types({
  "name": str,
  "description": str,
  "duration": int,
  "importance": int,
  "urgency": int,
  "categories": list
})
def create_task():
    try:
        session: Session = current_app.db.session
        EisenhowerModel.insert_values_if_not_exists()
        if not request.get_json():
            raise JSONNotFound
        
        data:dict = request.get_json()
        data_categories = [item.lower() for item in data['categories']]
        data.pop("categories")
        
        if((data['importance']) <1 or data['importance']>2): 
            raise ValueOutRange
        if(data['urgency'] <1 or data['urgency']>2): 
            raise ValueOutRange
        

        new_task = TasksModel(**data)
        new_task.query_eisenhower_id()
        for category_item in data_categories:
            category_item = category_item.lower()
            
            category = CategoryModel.query.filter_by(name=category_item).first()
            if not category:
                category = CategoryModel(**{"name": category_item})
            
            new_task.categories.append(category)

        session.add(new_task)
        session.commit()
        data:dict = {**new_task.asdict(),"categories": data_categories}

        return jsonify(**data),HTTPStatus.CREATED
    except ValueOutRange as e:
        return {
           "msg": {
                "valid_options": {
                "importance": [1, 2],
                "urgency": [1, 2]
                    }
            },
                "recieved_options": {
                    "importance": data['importance'],
                    "urgency": data['urgency']
            }
            },HTTPStatus.BAD_REQUEST
    except JSONNotFound as e:
        return {"error": "Body no have JSON"},HTTPStatus.UNPROCESSABLE_ENTITY
    except (UniqueViolation,IntegrityError):
       return { "msg": "task already exists!"},HTTPStatus.CONFLICT
    except Exception as e:
        raise e


def get_tasks():
    categorys :CategoryModel = CategoryModel.query.all()
    data=[]
    for categorie in categorys:
        data.append({**categorie.asdict(),"tasks": categorie.tasks})
        for item in categorie.tasks:
            item: TasksModel
            item.query_eisenhower_id()
    
    return jsonify(data), HTTPStatus.OK


def get_one_task(id:int):
    try:
        task: TasksModel = TasksModel.query.get(id)
        if not task:
            raise NoResultFound
        
        task.query_eisenhower_id()
        
        return jsonify(task),HTTPStatus.OK
    except NoResultFound:
        return {"error": "Not Found task."},HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e


def delete_tasks(id:int):
    try:
        session: Session = current_app.db.session
        task:TasksModel = TasksModel.query.get(id)
        if not task:
            raise NoResultFound

        session.delete(task)
        session.commit()

        return "",HTTPStatus.NO_CONTENT
    except NoResultFound:
        return {"error": "Not Found task."},HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e

def update_tasks(id:int):
    ...
    try:
        session: Session = current_app.db.session
        
        if not request.get_json():
            raise JSONNotFound
        
        task:TasksModel = TasksModel.query.get(id)
        if not task:
            raise NoResultFound
        task.query_eisenhower_id()
        data:dict = request.get_json()
        if(data.get("importance")):
            if((data['importance']) <1 or data['importance']>2): 
                raise ValueOutRange
        if(data.get("urgency")):
            if(data['urgency'] <1 or data['urgency']>2): 
                raise ValueOutRange
        data_categories = []
        if(data.get("categories")):
            data_categories = [item.lower() for item in data['categories']]
            data.pop("categories")
        
        for key,value in data.items():
            setattr(task,key,value)
        task.query_eisenhower_id()
        
        
        if(data_categories):
            for category_item in data_categories:
                category = CategoryModel.query.filter_by(name=category_item).first()
                if not category:
                    category = CategoryModel(**{"name": category_item})
            
            task.categories.append(category)
        session.add(task)
        session.commit()
        
        data_categories = [element.name for element in task.categories]
        data:dict = {**task.asdict(),"categories": data_categories}
        
        return jsonify(data),HTTPStatus.CREATED
    except ValueOutRange as e:
        return {
           "msg": {
                "valid_options": {
                "importance": [1, 2],
                "urgency": [1, 2]
                    }
            },
                "recieved_options": {
                    "importance": data['importance'],
                    "urgency": data['urgency']
            }
            },HTTPStatus.BAD_REQUEST
    except JSONNotFound as e:
        return {"error": "Body no have JSON"},HTTPStatus.UNPROCESSABLE_ENTITY
    except NoResultFound:
        return {"error": "Not Found task."},HTTPStatus.BAD_REQUEST
    except (UniqueViolation,IntegrityError):
       return { "msg": "task already exists!"},HTTPStatus.CONFLICT
    except Exception as e:
        raise e
