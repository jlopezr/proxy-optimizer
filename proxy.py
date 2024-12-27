#!/usr/bin/env python3
from fastapi import FastAPI, Request, Response
import httpx
import os
import optimize_css

app = FastAPI()
TARGET_SERVER = 'http://localhost:8000'

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(request: Request, path: str):
    client = httpx.AsyncClient()
    url = f"{TARGET_SERVER}/{path}"
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    print(f"Received {method} request for {url}")

    response = await client.request(method, url, headers=headers, content=body)

    # Check if the request ends in .css
    if url.endswith(".css") and response.status_code == 200:
        print("CSS file detected")
        # Remove the filename from the path
        dir = path.split("/")[:-1]
        # Create the path to the cache folder
        dir = "/".join(dir)

        print("PATH", path)
        print("DIRECTORY", dir)

        # Create the cache folder if it does not exist
        os.makedirs(f"cache/{dir}", exist_ok=True)

        # Store the file in a file in a cache folder following the url path
        with open(f"cache/{path}", "wb") as f:
            f.write(response.content)

        # Optimize the CSS file
        optimize_css.optimize_css_file(f"cache/{path}", f"cache/{path}")

        # Update content-length header
        response.headers["content-length"] = str(os.path.getsize(f"cache/{path}"))

        # Return the optimized CSS file
        with open(f"cache/{path}", "rb") as f:
            return Response(content=f.read(), status_code=response.status_code, headers=dict(response.headers))

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

    # build a 200 OK response
    #return {"result": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)