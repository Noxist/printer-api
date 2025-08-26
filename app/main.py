from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import api_routes, ui_routes

app = FastAPI(title="Printer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_routes.router, prefix="", tags=["API"])
app.include_router(ui_routes.router, prefix="", tags=["UI"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

