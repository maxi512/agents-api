import os
from agents import Agent


class ParseAPIAgent:
    """Agent that parses API responses and creates HeroModel objects."""
    
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or provided as argument")
        self.model = model
        self.agent = Agent(
            name="Parse API Agent",
            instructions="""
            You are an expert at parsing API responses and converting them into structured HeroModel objects.

            Your task is to analyze JSON responses from the Superhero API and extract the information needed to create HeroModel objects.

            The HeroModel structure requires:
            - name: string (the hero's name)
            - real_name: string (the hero's real name/alias, can be empty string if not found)
            - universe: string (must be either "Marvel" or "DC comics")

            API Response Structure:
            The Superhero API typically returns responses in this format:
            {
            "response": "success",
            "results": [
                {
                "name": "Hero Name",
                "biography": {
                    "full-name": "Real Name",
                    "alter-egos": "Alter Ego",
                    "publisher": "Marvel Comics" or "DC Comics"
                }
                }
            ]
            }

            Mapping Rules:
            1. Extract the "name" field directly from the result object
            2. Extract the "real_name" from biography["full-name"] or biography["alter-egos"] (use empty string if neither exists)
            3. Determine "universe" from biography["publisher"]:
            - If publisher contains "Marvel" → universe = "Marvel"
            - If publisher contains "DC" → universe = "DC comics"
            - Default to "Marvel" if publisher is unclear

            Output Format:
            Return a JSON array of HeroModel objects. Each object should have:
            {
            "name": "...",
            "real name": "...",  // Note: use "real name" (with space) as the key
            "universe": "Marvel" or "DC comics"
            }

            Handle edge cases:
            - If "results" is not an array, treat it as a single result
            - If "response" is not "success", return an empty array
            - If biography is missing, use empty string for real_name
            - Always return valid JSON, even if no heroes are found (return empty array)""",
            model=model,
        )
    
    def as_tool(self, tool_name: str = "parse_api_response", tool_description: str | None = None):
        """Return this agent as a tool for use in other agents."""
        description = tool_description or "Parse the API response and create HeroModel objects with the correct data mapping. Use this after calling the API to convert the response into the expected format."
        return self.agent.as_tool(
            tool_name=tool_name,
            tool_description=description,
        )

