import uvicorn
from fastapi import FastAPI

def main() -> None:
    app = FastAPI()

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
