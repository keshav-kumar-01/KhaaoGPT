"""
KhaoGPT — Local development entry point.
Passes all execution to api/index.py for parity with Vercel.
"""
from api.index import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
