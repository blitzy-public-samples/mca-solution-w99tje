from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.database import get_db
from src.core.security import get_current_user
from src.api.routes import application_routes, document_routes, user_routes, webhook_routes

app = FastAPI()

def configure_cors():
    # Configure CORS settings for the application
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def include_routers():
    # Include all API routers in the main application
    app.include_router(application_routes.router, prefix="/applications")
    app.include_router(document_routes.router, prefix="/documents")
    app.include_router(user_routes.router, prefix="/users")
    app.include_router(webhook_routes.router, prefix="/webhooks")

@app.on_event("startup")
async def startup_event():
    # Log application startup
    print("Application is starting up...")
    # Perform any necessary initialization tasks
    configure_cors()
    include_routers()

@app.on_event("shutdown")
async def shutdown_event():
    # Log application shutdown
    print("Application is shutting down...")
    # Perform any necessary cleanup tasks

@app.get("/")
async def root():
    # Return a welcome message and the API version from settings
    return {
        "message": "Welcome to the MCA Application Processing System API",
        "version": settings.API_VERSION
    }

# Human tasks:
# 1. Review and update CORS settings in the configure_cors function if necessary
# 2. Add any additional initialization tasks in the startup_event function
# 3. Add any necessary cleanup tasks in the shutdown_event function
# 4. Review and update the root endpoint message if needed