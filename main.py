import uvicorn
from fastapi import FastAPI
from public.study import router
from database import create_async_tables, init_db
from datetime import datetime

app = FastAPI()
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await init_db()
    await create_async_tables()
    with open("log.txt", mode="a") as f:
        f.write(f"Приложение запущено: {datetime.now()}\n")



@app.on_event("shutdown")
def shutdown_event():
     with open("log.txt", mode="a") as f:
         f.write(f"Приложение остановлено: {datetime.now()}\n")

@app.get("/")
def index():
    return "FastApi 3"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)