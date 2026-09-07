from fastapi import FastAPI

app = FastAPI(
    title="FlyRank Auth API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "FlyRank Auth API is running"
    }


@app.get("/public/info")
def public_info():
    return {
        "message": "This is a public endpoint"
    }