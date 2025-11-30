def main():
    print("Hello from minicrm!")


if __name__ == "__main__":
    main()


# app/main.py
from fastapi import FastAPI

from app.api import router as api_router

app = FastAPI(
    title="MiniCRM Test",
    version="666",
)

app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}