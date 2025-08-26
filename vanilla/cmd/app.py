from fastapi import FastAPI
from vanilla.pkg.routers import user_routes
from vanilla.pkg.database.database import Base, engine

app = FastAPI()

# Pastikan model dikenali
Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)

