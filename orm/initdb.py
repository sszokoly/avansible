from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///main.db', echo=True)
Base = declarative_base()

class Ansible_Parent_Group(Base):
    __tablename__ = 'ansible_parent_group'

    group_name =  Column(String(), primary_key=True)
    descr = Column(String())
    vendor = Column(String())

class Ansible_Child_Group(Base):
    __tablename__ = 'ansible_child_group'

    group_name =  Column(String(), primary_key=True)
    descr = Column(String())
    parent_group_name = Column(
        String(),
        ForeignKey(
            'ansible_parent_group.group_name', 
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        nullable=True,
    )

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

#parent1 = Ansible_Parent_Group(group_name="SMGR", descr="System Manager", vendor="Avaya")
#parent2 = Ansible_Parent_Group(group_name="SM", descr="Session Manager", vendor="Avaya")
child1 = Ansible_Child_Group(group_name="asm", descr="Core Session Manager", parent_group_name="SM")
#child2 = Ansible_Child_Group(group_name="SM", descr="Session Manager", vendor="Avaya")

#session.add(parent1)
#session.add(parent2)
session.add(child1)
session.commit()
