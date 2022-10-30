import sqlalchemy.sql as sql
from sqlalchemy import Column, String, Integer, DateTime
from datetime import date
from .conn import Base, Session, engine
from .utils import row_to_dict

class Events(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}

    event_id = Column(Integer, primary_key=True)
    user_id = Column(String)
    datetime = Column(DateTime)

    @row_to_dict
    def find_all(id_from: int=1, id_to: int=100):
        with Session.begin() as session:
            res = session.query(Events).where(
                Events.event_id.between(id_from, id_to)
            )
        return res.all()
    
    @row_to_dict
    def get_count_by_day(date_from: date, date_to: date) -> list:
        with Session.begin() as session:
            date = cast(Events.datetime, Date)
            res = session.query(
                date.label("date"),
                func.count(Events.event_id).label("count")
            ).where(
                date.between(date_from, date_to)
            ).group_by(date)
        return res.all()
    
    def save(self) -> None:
        with Session.begin() as session:
            session.add(self)

Base.metadata.create_all(engine)
