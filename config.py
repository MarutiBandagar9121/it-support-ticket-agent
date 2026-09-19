import dotenv
import os

dotenv.load_dotenv()

class Config:
    def __init__(self):
        self.open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY")

settings = Config()