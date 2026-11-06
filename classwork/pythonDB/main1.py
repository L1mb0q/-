from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, DeclarativeBase

engine = create_engine("sqlite:///university.sqlite.db")

class Base(DeclarativeBase): pass
class Groups(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    course = Column(Integer)


with Session(autoflush=False, bind=engine) as db:
    groups = db.query(Groups).all()
    for group in groups:
        print(f"ID:{group.group_id} Название группы: {group.group_name} Курс: {group.course}")