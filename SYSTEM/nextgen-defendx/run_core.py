import uvicorn
from core.main import app   # only change

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)