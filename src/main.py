import os
from typing import Union, Literal
from datetime import datetime, date, timedelta
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from common import auth, firestore, utils
from db import Events, EventType, dbexc
from middlewares import IdTokenMiddleware
from middlewares.datadog_event import DatadogEventMiddleware
from datadog import initialize, statsd

initialize(statsd_host="127.0.0.1", statsd_port=8125)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.add_middleware(IdTokenMiddleware)
app.add_middleware(DatadogEventMiddleware)

@app.get("/")
async def get_events(
        max_results: Union[int, None] = 10,
        page_token: Union[int, None] = None,
    ):
    """
    List up to max_results recent events.
    """
    try:
        events = Events.find_all(page_token, max_results)
    except dbexc.OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    n_results = len(events)
    more_results = n_results >= max_results
    return {
        "result": events,
        "page_token": (events[-1]["event_id"]) if more_results else None
    }

@app.post("/{event_type}")
async def create_event(uid: str, event_type: EventType):
    """
    Create a new login event.
    """
    event = Events(user_id=uid, event_type=event_type, datetime=datetime.now())
    try:
        event.save()
    except dbexc.OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/stats")
async def get_stats():
    date_to = date.today()
    date_from = date_to - timedelta(days=15)
    try:
        stats = {
            event_type.value: Events.get_count_by_day(
                event_type.value,
                date_from,
                date_to
            )
            for event_type in EventType
        }
    except dbexc.OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    return {"result": stats}

@app.get("/usersSummary")
async def get_users_summary():
    return {
        "result": {
            "total_users": utils.get_user_count(),
            "total_admins": utils.get_admin_count(),
            "total_blocked_users": utils.get_blocked_user_count()
        }
    }
