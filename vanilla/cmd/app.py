from fastapi import FastAPI
from vanilla.pkg.routers import user_routes, service_routes
from vanilla.pkg.database.database import Base, engine

app = FastAPI()

# Auto migration  
Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(service_routes.router)

