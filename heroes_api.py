import os
import requests

class SuperheroAPIClient:
    
    BASE_URL = "https://www.superheroapi.com/api.php"
    
    def __init__(self, api_key: str | None = None, timeout: float = 10.0):
        self.api_key = api_key or os.getenv("SUPERHERO_API_KEY")
        if not self.api_key:
            raise ValueError("SUPERHERO_API_KEY not found in environment variables or provided as argument")
        
        self.timeout = timeout
    
    def search_hero(self, name: str) -> dict:
        """Search for a hero by name."""
        url = f"{self.BASE_URL}/{self.api_key}/search/{name}"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
