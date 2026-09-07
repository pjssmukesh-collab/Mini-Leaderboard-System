# app/main.py
# ──────────────────────────────────────────────
# Main FastAPI Application Entry Point
#
# This is the SAME app from Prompt 1, but now it lives inside the
# app/ package. It imports settings from config.py and is structured
# to cleanly include routers as we add them in future prompts.
#
# Run with: uvicorn app.main:app --reload
# (run from the backend/ directory)
# ──────────────────────────────────────────────

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# ──────────────────────────────────────────────
# Create the FastAPI application
# ──────────────────────────────────────────────
# Now we pull the app name, description, and version from our
# centralized config instead of hard-coding them.
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# ──────────────────────────────────────────────
# CORS Middleware
# ──────────────────────────────────────────────
# CORS = Cross-Origin Resource Sharing
#
# Problem: Your React frontend runs on http://localhost:3000
#          Your FastAPI backend runs on http://localhost:8000
#          Browsers BLOCK requests between different origins by default.
#
# Solution: This middleware tells the browser "it's okay, allow
#           requests from these origins."
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Which frontends can talk to us
    allow_credentials=True,                # Allow cookies
    allow_methods=["*"],                   # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                   # Allow all headers
)


# ──────────────────────────────────────────────
# Include Routers
# ──────────────────────────────────────────────
from app.routers import auth_router, events_router, rules_router, participants_router, uploads_router, validation_router, leaderboard_router

app.include_router(auth_router)
app.include_router(events_router)
app.include_router(rules_router)
app.include_router(participants_router)
app.include_router(uploads_router)
app.include_router(validation_router)
app.include_router(leaderboard_router)




# ──────────────────────────────────────────────
# Route 1: GET /
# ──────────────────────────────────────────────
# The "home" route — confirms the API is running.
@app.get("/", tags=["General"])
def root():
    return {"message": f"{settings.APP_NAME} API is running"}


# ──────────────────────────────────────────────
# Route 2: GET /health
# ──────────────────────────────────────────────
# Health check endpoint — monitoring tools use this to verify
# the server is alive.
@app.get("/health", tags=["General"])
def health_check():
    return {"status": "healthy"}
