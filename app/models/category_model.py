from dataclasses import asdict, dataclass

from sqlalchemy import Column
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.orm import relationship, validates


from app.configs.database import db

@dataclass
class CategoryModel(db.Model):
    id: int
    name : str
    description: str

    __tablename__ = "categories"
    
    id = Column(sql.Integer,primary_key=True)
    name = Column(sql.String(100),nullable=False, unique=True)
    description = Column(sql.Text)

    def asdict(self)-> dict:
        return asdict(self)
    
    @validates("name")
    def validate_in_title(self,key:str,value:str)-> None:
        return value.lower()
    
    def serializer(self):
        return {"name": self.name}

 