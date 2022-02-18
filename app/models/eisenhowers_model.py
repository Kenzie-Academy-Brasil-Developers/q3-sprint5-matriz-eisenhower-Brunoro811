from dataclasses import dataclass
from flask import current_app

from sqlalchemy import Column
from sqlalchemy.sql import sqltypes as sql
from app.configs.database import db

from sqlalchemy.orm import Session

@dataclass
class EisenhowerModel(db.Model):
    id: int
    type : str

    __tablename__ = "eisenhowers"
    id = Column(sql.Integer, primary_key=True)
    type= Column(sql.String(100))

    @classmethod
    def insert_values_if_not_exists(cls):
        session: Session = current_app.db.session
        default_values = ["Do It First","Schedule It","Delegate It","Delete It"]
        values = EisenhowerModel.query.all()
        list_values_insert = []
        if not values:
            for value in default_values:
                value_insert = EisenhowerModel(**{"type":value})
                list_values_insert.append(value_insert)
            session.add_all(list_values_insert)
            session.commit()
