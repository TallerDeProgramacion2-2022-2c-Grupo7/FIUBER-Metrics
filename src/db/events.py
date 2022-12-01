import sqlalchemy.sql as sql
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import cast, Date
from sqlalchemy import func
from datetime import date
from typing import Union
from .conn import Base, Session
from .utils import db_method
from enum import Enum

class EventType(str, Enum):
    signup = "signup"
    login = "login"
    password_reset = "passwordReset"
    federated_login = "federatedLogin"
    block = "block"
    unblock = "unblock"

class Events(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}

    event_id = Column(Integer, primary_key=True)
    user_id = Column(String)
    event_type = Column(String)
    datetime = Column(DateTime)

    def __iter__(self):
        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                yield key, value

    @db_method
    def find_all(
            id_from: Union[int, None] = None,
            max_results: int = 10
        ) -> list:
        with Session.begin() as session:
            query = session.query(Events)
            if id_from is not None:
                query = query.where(Events.event_id < id_from)
            res = query.order_by(Events.event_id.desc()).limit(max_results)
        return res.all()

    @db_method
    def get_count_by_day(
            event_type: str,
            date_from: date,
            date_to: date
        ) -> list:
        with Session.begin() as session:
            date = cast(Events.datetime, Date)
            res = session.query(
                date.label("date"),
                func.count(Events.event_id).label("count")
            ).where(
                (date.between(date_from, date_to))
                & (Events.event_type == event_type)
            ).group_by(date)
        return res.all()

    @db_method
    def save(self) -> None:
        with Session.begin() as session:
            session.add(self)
