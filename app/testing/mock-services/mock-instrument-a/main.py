from fastapi import FastAPI
import time
import random

app = FastAPI(title="Mock Instrument A")


@app.post("/start_analysis")
async def start_analysis(sample_id: str):
    # Simulate processing time
    await asyncio.sleep(random.uniform(1, 5))
    return {
        "status": "completed",
        "sample_id": sample_id,
        "results": {"concentration": random.uniform(0.1, 10.0)},
    }
