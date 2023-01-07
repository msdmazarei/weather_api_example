"""
Main Module for defining and running web appliation
"""
import uvicorn

from app import web_app

if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", port=8000)
