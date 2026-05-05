import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUR_NICHE = "IA et Cybersécurité"
YOUR_LANGUAGE = "français"
YOUR_TONE = "expert accessible, direct, concret — pas de jargon inutile"
TARGET_AUDIENCE = "professionnels tech, décideurs IT, passionnés IA — marché DACH et francophone"