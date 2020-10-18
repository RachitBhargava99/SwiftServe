from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import yaml

from db import models
from db.db import engine
from api.api import api_router
from etc.usrmng import initialize_fastapi_users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwiftServe", docs_url='/')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.openapi_schema = yaml.load(open('swagger.yaml').read())
initialize_fastapi_users(app)
app.include_router(api_router)
