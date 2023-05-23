from sqlalchemy import create_engine, ForeignKey, select, delete, event
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///main.db', echo=False)
Base = declarative_base()

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Ansible_Parent_Group(Base):
    __tablename__ = 'ansible_parent_group'

    group_name =  Column(String(), primary_key=True)
    descr = Column(String())
    vendor = Column(String())

class Ansible_Child_Group(Base):
    __tablename__ = 'ansible_child_group'

    group_name =  Column(String(), primary_key=True)
    descr = Column(String())
    parent_group_name = Column(String(), ForeignKey('ansible_parent_group.group_name'), nullable=True)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

parent1 = Ansible_Parent_Group(group_name="SMGR", descr="System Manager", vendor="Avaya")
parent2 = Ansible_Parent_Group(group_name="SM", descr="Session Manager", vendor="Avaya")
child1 = Ansible_Child_Group(group_name="asm", descr="Core Session Manager", parent_group_name="SM")
child2 = Ansible_Child_Group(group_name="bsm", descr="Branch Session Manager", parent_group_name="SM")

session.add(parent1)
session.add(parent2)
session.commit()
session.add(child1)
session.add(child2)
session.commit()
SM = session.get(Ansible_Parent_Group, "SM")
session.delete(SM)
session.flush()
for group in session.query(Ansible_Parent_Group).all():
    print(vars(group))
for group in session.query(Ansible_Child_Group).all():
    print(vars(group))