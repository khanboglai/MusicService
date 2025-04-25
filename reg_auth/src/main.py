from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# app.include_router(login.router)
# app.include_router(register.router)

@app.get("/")
def idx():
    return "Hello"

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

#python3 -m uvicorn main:app
# 127.0.0.1:8000/docs