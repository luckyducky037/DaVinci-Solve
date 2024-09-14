import pvorca
from groq import Groq
from dotenv import load_dotenv
from os import getenv

load_dotenv()

groq_client = Groq(api_key=getenv("GROQ"))
orca_client = pvorca.create(access_key=getenv("ORCA"))