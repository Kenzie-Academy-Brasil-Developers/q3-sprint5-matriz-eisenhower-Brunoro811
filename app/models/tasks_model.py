from dataclasses import asdict, dataclass

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship,validates

from app.configs.database import db
from app.models.eisenhowers_model import EisenhowerModel


@dataclass
class TasksModel(db.Model):
    id: int
    name: str
    description: str
    duration: int
    classitication: str = None


    __tablename__ = "tasks"
    id = Column(sql.Integer, primary_key=True)
    name = Column(sql.String(100),nullable=False,unique=True)
    description = Column(sql.Text)
    duration= Column(sql.Integer)
    importance= Column(sql.Integer)
    urgency = Column(sql.Integer)
    eisenhower_id = Column(sql.Integer,ForeignKey("eisenhowers.id"))
    
    categories = relationship("CategoryModel",secondary="task_categories", backref="tasks")


    def asdict(self):
        return asdict(self)

    def query_eisenhower_id(self)-> None:
        table =  {
        "11": "Do It First",
        "12": "Delegate It",
        "21": "Schedule It",
        "22": "Delete It",
        }
        key = f"{self.importance}{self.urgency}"
        search = table[key]
        result: EisenhowerModel = EisenhowerModel.query.filter_by(type=search).first()
        self.classitication = result.type
        self.eisenhower_id =  result.id
        

    @validates("name")
    def validate_in_title(self,key:str,value:str)-> None:
        return value.lower()