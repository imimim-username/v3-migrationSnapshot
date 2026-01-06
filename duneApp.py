from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

graphApiKey = os.getenv("GRAPH_API_KEY")
    thousand = str(multiplier * 1000)

    headers = {
        "Content-Type": "application/json"
    }