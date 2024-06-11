from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import routes
from .utils import configure_error_handlers
from .responses import PrettyJSONResponse

app = FastAPI(default_response_class=PrettyJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

[app.include_router(route) for route in routes]
[app.add_exception_handler(exc, handler) for exc, handler in configure_error_handlers().items()]