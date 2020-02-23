#!/usr/bin/env python                       
# -*- coding:utf-8 -*-                              

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Test(Base):
    """
    测试表
    """
    __tablename__ = 'test_model'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    language = Column(String(32), nullable=False)
    type = Column(String(32), nullable=False)

    def __repr__(self):
        return f"<{self.id} model.name: {self.name}>"

