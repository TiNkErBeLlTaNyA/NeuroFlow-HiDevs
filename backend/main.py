from fastapi import FastAPI
import asyncpg
import redis.asyncio as redis
import os
import asyncio

app = FastAPI(title="NeuroFlow API", version="1.0.0")


# -------------------------------
# Wait for dependencies
# -------------------------------

async def wait_for_postgres():
    while True:
        try:
            conn = await asyncpg.connect(
                user="neuroflow",
                password=os.getenv("POSTGRES_PASSWORD"),
                database="neuroflow",
                host="postgres"
            )
            await conn.close()
            print("Postgres ready")
            break
        except Exception:
            print("Waiting for Postgres...")
            await asyncio.sleep(2)


async def wait_for_redis():
    while True:
        try:
            r = redis.Redis(
                host="redis",
                port=6379,
                password=os.getenv("REDIS_PASSWORD")
            )
            await r.ping()
            print("Redis ready")
            break
        except Exception:
            print("Waiting for Redis...")
            await asyncio.sleep(2)


# -------------------------------
# Startup
# -------------------------------

@app.on_event("startup")
async def startup():
    await wait_for_postgres()
    await wait_for_redis()

    app.state.pg = await asyncpg.create_pool(
        user="neuroflow",
        password=os.getenv("POSTGRES_PASSWORD"),
        database="neuroflow",
        host="postgres",
        min_size=1,
        max_size=5
    )

    app.state.redis = redis.Redis(
        host="redis",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

    print("Startup complete")


# -------------------------------
# Shutdown
# -------------------------------

@app.on_event("shutdown")
async def shutdown():
    await app.state.pg.close()
    await app.state.redis.aclose()   # ✅ FIXED
    print("Shutdown complete")


# -------------------------------
# Health (resilient)
# -------------------------------

@app.get("/health")
async def health():
    checks = {}

    try:
        async with app.state.pg.acquire() as conn:
            await conn.execute("SELECT 1")
        checks["postgres"] = True
    except:
        checks["postgres"] = False

    try:
        await app.state.redis.ping()
        checks["redis"] = True
    except:
        checks["redis"] = False

    return {
        "status": "ok" if all(checks.values()) else "degraded",
        "checks": checks
    }


# -------------------------------
# Root
# -------------------------------

@app.get("/")
async def root():
    return {"message": "NeuroFlow API is running"}