from dotenv import load_dotenv
import os
import requests
import pandas as pd

from runDuneQuery import updateQuery, getQuery #(inputID)

print(getQuery(6475554))