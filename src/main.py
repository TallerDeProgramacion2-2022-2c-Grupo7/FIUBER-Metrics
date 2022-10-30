import os
from typing import Union, Literal
from datetime import datetime, date, timedelta
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from common import auth, firestore
from db import Events
from middlewares import IdTokenMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.add_middleware(IdTokenMiddleware)

@app.get("/")
async def get_events(
        max_results: Union[int, None] = 100,
        page_token: Union[int, None] = 1,
    ):
    """
    List up to max_results recent events.
    """
    events = Events.find_all(page_token, page_token + max_results - 1)
    n_results = len(events)
    more_results = n_results >= max_results
    return {
        "result": events,
        "page_token": (page_token + n_results) if more_results else None
    }

@app.post("/{event_type}")
async def create_event(
        uid: str,
        event_type: Literal["signup", "login", "passwordReset"]
    ):
    """
    Create a new login event.
    """
    event = Events(user_id=uid, event_type=event_type, datetime=datetime.now())
    event.save()

@app.get("/stats")
async def get_stats():
    date_to = date.today()
    date_from = date_to - timedelta(days=15)
    stats = {
        event_type: Events.get_count_by_day(event_type, date_from, date_to)
        for event_type in ("signup", "login", "passwordReset")
    }
    return {"result": stats}
