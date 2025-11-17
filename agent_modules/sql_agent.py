import os
from agents import Agent, Runner

class SQLAgent:
    """Agent that generates SQL queries from natural language using OpenAI Agents SDK."""
    
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or provided as argument")
        
        self.model = model

        self.agent = Agent(
            name="SQL Agent",
            instructions="""
            You are a SQL expert. Generate SQL queries for a heroes database.

            The heroes table has the following columns:
            - id (INTEGER, primary key)
            - name (TEXT)
            - alias (TEXT, nullable) - the real name of the hero
            - universe (TEXT) - either 'DC comics' or 'Marvel'

            Rules:
            - Always use SELECT * FROM heroes WHERE ...
            - Use proper SQL syntax for SQLite
            - For text comparisons, use LIKE for partial matches or = for exact matches
            - Return ONLY the SQL query, nothing else
            - Do not include any explanations or markdown formatting
            - Use single quotes for string literals
            """,
            model=model,
        )
    
    def generate_sql(self, query: str) -> str:
        """Generate SQL from natural language query."""
        import asyncio
        
        async def _generate():
            result = await Runner.run(
                self.agent,
                input=f"Generate SQL for: {query}",
            )
            sql = result.final_output.strip()
            # Clean up markdown code blocks if present
            if sql.startswith("```sql"):
                sql = sql[6:]
            elif sql.startswith("```"):
                sql = sql[3:]
            if sql.endswith("```"):
                sql = sql[:-3]
            return sql.strip()
        
        return asyncio.run(_generate())
    
    def as_tool(self, tool_name: str = "generate_sql", tool_description: str | None = None):
        """Return this agent as a tool for use in other agents."""
        description = tool_description or "Generate a SQL query from natural language. Use this when the user wants to search the heroes database."
        return self.agent.as_tool(
            tool_name=tool_name,
            tool_description=description,
        )


_agent = None

def generate_sql(query: str) -> str:
    """Convenience function to generate SQL."""
    global _agent
    if _agent is None:
        _agent = SQLAgent()
    return _agent.generate_sql(query)

