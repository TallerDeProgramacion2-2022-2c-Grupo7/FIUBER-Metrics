import os
from typing import Union
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from common.firebase_admin import auth, firestore
from db.events import Events
from middlewares.id_token import IdTokenMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# app.add_middleware(IdTokenMiddleware)

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

@app.post("/")
async def create_event(uid: str, event_type: str):
    """
    Create a new login event.
    """
    event = Events(user_id=uid, datetime=datetime.now())
    event.save()
