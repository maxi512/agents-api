import sqlite3
from typing import List, Dict, Any
from pathlib import Path
from agents import function_tool

from heroes_api import SuperheroAPIClient
from models import HeroModel
from heroes_database import DB_PATH


@function_tool
def execute_sql(sql: str) -> List[Dict[str, Any]]:
    """Execute a SQL SELECT query on the heroes database. Use this ONLY for HEROES. The database contains heroes with columns: id, name, alias (real name), universe. Villains are NOT in the database."""
    print(f'Executing {sql}')
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        heroes = []
        for row in rows:
            hero_model = HeroModel(
                id=row['id'],
                name=row['name'],
                real_name=row['alias'] or "",
                universe=row['universe']
            )
            heroes.append(hero_model.model_dump(by_alias=True))
        return heroes
    finally:
        conn.close()


@function_tool
def call_api(hero_name: str) -> Dict[str, Any]:
    """Call the Superhero API to search for a character. Use this ONLY for VILLAINS. Heroes should be queried from the database using generate_sql and execute_sql tools."""
    print(f'Calling the API with {hero_name}')
    api_client = SuperheroAPIClient()
    return api_client.search_hero(hero_name)
