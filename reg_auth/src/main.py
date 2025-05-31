import asyncio
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import uvicorn

from src.api import register, login, me, admin
from src.grpc.server import serve


@asynccontextmanager
async def lifespan(_: FastAPI):
    asyncio.create_task(serve())
    yield

app = FastAPI(
    lifespan=lifespan,
)

app.include_router(register.router)
app.include_router(login.router)
app.include_router(me.router)
app.include_router(admin.router)


@app.get("/")
def idx():
    return "Hello"

if __name__ == '__main__':
    uvicorn.run("src.main:app", reload=True)

#python3 -m uvicorn main:app
# 127.0.0.1:8000/docs127.0.0.1:8000