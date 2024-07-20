import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.config import app_setting
from api.v1 import users, weather



app = FastAPI(
    docs_url="/api/openapi",
    default_response_class=ORJSONResponse
)

origin = [
    "http://localhost",
    "http://localhost:5173"
]

app.include_router(router=users.router, prefix="/api/v1", tags=["users"])
app.include_router(router=weather.router, prefix="/api/v1", tags=["weather"])


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=app_setting.project_host,
        port=app_setting.project_port
    )
