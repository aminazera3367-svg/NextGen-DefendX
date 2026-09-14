# start.py
import sys
import os

# Add the 'core' directory to Python's path
sys.path.insert(0, os.path.join(os.getcwd(), 'core'))

# Import and run the app
from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)