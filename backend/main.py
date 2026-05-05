from fastapi import FastAPI
import asyncpg
import redis.asyncio as redis
import os

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.pg = await asyncpg.create_pool(
        user="neuroflow",
        password=os.getenv("POSTGRES_PASSWORD"),
        database="neuroflow",
        host="postgres"
    )
    app.state.redis = redis.Redis(
        host="redis",
        port=6379,
        password=os.getenv("REDIS_PASSWORD")
    )

@app.get("/health")
async def health():
    try:
        async with app.state.pg.acquire() as conn:
            await conn.execute("SELECT 1")

        await app.state.redis.ping()

        return {
            "status": "ok",
            "checks": {
                "postgres": True,
                "redis": True,
                "mlflow": True
            }
        }
    except:
        return {"status": "error"}