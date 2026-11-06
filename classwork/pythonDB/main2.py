from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, relationship

engine = create_engine("sqlite:///university.sqlite.db")

class Base(DeclarativeBase): pass
class Groups(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    course = Column(Integer)

class Students(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    group = relationship("Groups")


with Session(autoflush=False, bind=engine) as db:
    students = db.query(Students).all()
    for student in students:
        print(f"ID:{student.student_id} ФИ: {student.last_name} {student.first_name} Группа:{student.group.group_name}")