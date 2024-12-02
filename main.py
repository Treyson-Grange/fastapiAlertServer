#!/usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.routes import alert_router

load_dotenv()

allowed_origins = os.getenv("ALLOWED_ORIGINS").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["API-Key", "Content-Type", "Authorization"],
)

app.include_router(alert_router)
