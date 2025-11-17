from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from typing import List
from heroes_database import init_database
from agent_modules.hero_agent import HeroAgent
from models import HeroModel

load_dotenv(override=True)

init_database()

app = FastAPI()

@app.get("/heroes", response_model=List[HeroModel])
async def query_heroes(query: str):
    """Query heroes/villains using the hero agent."""
    try:
        agent = HeroAgent()
        return await agent.query_async(query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
