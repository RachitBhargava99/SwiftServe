from fastapi import FastAPI

import yaml

from db import models
from db.db import engine
from api.api import api_router
from etc.usrmng import initialize_fastapi_users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwiftServe", docs_url='/')
app.openapi_schema = yaml.load(open('swagger.yaml').read())
initialize_fastapi_users(app)
app.include_router(api_router)
