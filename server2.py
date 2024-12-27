#!/usr/bin/env python3
from sanic import Sanic, response
from sanic.response import file
import os
import hashlib

app = Sanic("FileServer")

# Get the script's directory
DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = os.path.join(DIR, "examples")

def generate_etag(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()
    return hashlib.md5(file_content).hexdigest()

@app.middleware('response')
async def add_etag(request, response):
    etag = None
    if response.status == 200 and response.body:
        etag = hashlib.md5(response.body).hexdigest()
        response.headers['ETag'] = etag
    if etag:
        print(f"{response.status} for {request.method} request to {request.url}. ETAG is {etag}")
    else:
        print(f"{response.status} for {request.method} request to {request.url}")

@app.middleware('request')
async def log_request(request):
    if_none_match = request.headers.get('if-none-match')
    if if_none_match:
        print(f"Received {request.method} request for {request.url} with If-None-Match {if_none_match}")
    else:
        print(f"Received {request.method} request for {request.url}")

@app.route("/<filename:path>")
async def serve_file(request, filename):
    file_path = os.path.join(EXAMPLES_DIR, filename)
    if os.path.isfile(file_path):
        etag = generate_etag(file_path)
        if_none_match = request.headers.get('if-none-match')
        if if_none_match == etag:
            return response.empty(status=304)
        return await file(file_path)
    else:
        return response.text("File not found", status=404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)