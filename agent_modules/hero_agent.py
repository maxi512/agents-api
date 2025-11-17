import os
from typing import List
from agents import Agent, Runner

from agent_modules.sql_agent import SQLAgent
from agent_modules.parse_api_agent import ParseAPIAgent
from agent_modules.tools import execute_sql, call_api
from models import HeroModel

class HeroAgent:
    
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or provided as argument")
        
        self.model = model
        self.sql_agent = SQLAgent(api_key=self.api_key, model=model)
        self.parse_agent = ParseAPIAgent(api_key=self.api_key, model=model)
        
        self.agent = Agent(
            name="Hero Agent",
            output_type=List[HeroModel],
            instructions="""You are a helpful assistant that can help users query a heroes database and fetch additional information from external APIs.

            You have access to tools that can:
            1. Generate SQL queries from natural language
            2. Execute SQL queries and return results
            3. Call the Superhero API to get detailed hero information
            4. Parse API responses and create HeroModel objects

            ⚠️ CRITICAL ROUTING LOGIC:

            1. DETECT IF QUERY IS FOR A SINGLE CHARACTER:
               - If the user asks for ONE specific character (e.g., "find Batman", "get Spider-Man", "show me Superman"), 
                 you MUST return a list with EXACTLY ONE HeroModel object.
               - If the user asks for multiple characters or a category (e.g., "all Marvel heroes", "DC heroes"), 
                 return a list with all matching results.

            2. HERO vs VILLAIN DETECTION:
               - IF HERO: Use the DATABASE (generate_sql + execute_sql tools)
                 * Heroes are stored in the database
                 * Use generate_sql to create a SQL query from the natural language
                 * Use execute_sql to run the query and get results
                 * The database contains heroes with: id, name, alias (real name), universe
               
               - IF VILLAIN: Use the API (call_api + parse_api_response tools)
                 * Villains are NOT in the database, only heroes are stored there
                 * You MUST use the call_api tool to search for villains
                 * You can and SHOULD call the API MULTIPLE TIMES if needed to find the correct villain
                 * After calling the API, use the parse_api_response tool to convert the response into HeroModel format
                 * Do NOT attempt to query the database for villains - they are not stored there

            3. RETURN FORMAT:
               - Always return a list of HeroModel objects
               - If query is for a single character, return a list with exactly ONE item
               - If query is for multiple characters, return a list with all matching items
               - If no results found, return an empty list""",
            tools=[
                self.sql_agent.as_tool(
                    tool_name="generate_sql",
                    tool_description="Generate a SQL query from natural language. Use this ONLY for HEROES. The database contains heroes with columns: id, name, alias (real name), universe. Use this tool when searching for heroes in the database."
                ),
                self.parse_agent.as_tool(
                    tool_name="parse_api_response",
                    tool_description="Parse the API response and create HeroModel objects with the correct data mapping. Use this after calling the API to convert the response into the correct format. Use this for VILLAINS."
                ),
                execute_sql,
                call_api,
            ],
            model=model,
        )
    
    async def query_async(self, user_query: str) -> List[HeroModel]:
        """Query the agent. Returns a list of HeroModel objects."""
        result = await Runner.run(self.agent, user_query)
        return result.final_output

