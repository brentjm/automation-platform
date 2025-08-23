from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading

# from .core.config import settings
from .core.database import init_db
from .api.v1 import workflows, tasks, webhooks
from .services.handlers.notification_listener import NotificationListener


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()

    # Start notification listener in background thread
    notification_listener = NotificationListener()
    listener_thread = threading.Thread(
        target=notification_listener.start_listener, daemon=True
    )
    listener_thread.start()

    yield
    # Shutdown
    pass


app = FastAPI(
    title="Laboratory Automation Framework",
    description="A framework for managing laboratory workflows and tasks",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflows.router)
app.include_router(tasks.router)
app.include_router(webhooks.router)
