# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref

from analysis_interface import Base


class ShoppingList(Base):
    __tablename__ = 'shopping_list'

    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    store_name = Column(String(1000))
    created_date = Column(DateTime, default=datetime.now())

    # association proxy of "shopping_list_items" collection to "item" attribute
    items = association_proxy('shopping_list_items', 'item')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ShoppingListKeyWord(Base):
    __tablename__ = 'shopping_list_item'

    shopping_list_id = Column(Integer, ForeignKey('shopping_list.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    quantity = Column(Integer, default=0)

    # bidirectional attribute/collection of "shopping_list"/"shopping_list_items"
    shopping_list = relationship(ShoppingList,
                                 backref=backref("shopping_list_items",
                                                 cascade="all, delete-orphan")
                                 )

    # reference to the "KeyWord" object
    item = relationship("KeyWord")

    def __init__(self, shopping_list=None, item=None, quantity=None):
        self.shopping_list = shopping_list
        self.item = item
        self.quantity = quantity

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'shopping_list_id'}


class KeyWord(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(1000))

    def __eq__(self, other):
        return self.id == other.id
