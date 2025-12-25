from fastapi import FastAPI
from api.routes import health, generate
from api.auth import routes as auth_routes

app = FastAPI(
    title="NEXTYOU API",
    version="0.1.0",
    description="AI SaaS Backend"
)

# routes
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(generate.router, prefix="/generate", tags=["AI"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

