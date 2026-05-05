import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_web(query: str, num_results: int = 5) -> list[dict]:
    """
    Recherche web via Serper API (Google Search).
    Retourne une liste de résultats avec titre, snippet, url.
    """
    
    if not SERPER_API_KEY:
        print("⚠️  Pas de clé Serper — mode sans recherche web.")
        return []
    
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "num": num_results,
        "hl": "fr",
        "gl": "de"  # Résultats géolocalisés Allemagne
    }
    
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload,
            timeout=10
        )
        data = response.json()
        
        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "url": item.get("link", "")
            })
        return results
        
    except Exception as e:
        print(f"⚠️  Erreur recherche web : {e}")
        return []


def extract_facts(topic: str, search_results: list[dict]) -> str:
    """
    Formate les résultats de recherche en contexte factuel
    utilisable par GPT.
    """
    
    if not search_results:
        return "Aucun fait externe disponible — génère sans statistiques inventées."
    
    facts = f"FAITS RÉELS sur '{topic}' (sources vérifiées) :\n\n"
    
    for i, result in enumerate(search_results[:4], 1):
        facts += f"Source {i} : {result['title']}\n"
        facts += f"Extrait : {result['snippet']}\n"
        facts += f"URL : {result['url']}\n\n"
    
    facts += "\nUTILISE CES FAITS. Ne cite que ce qui est présent ici. Si aucun chiffre n'est disponible, n'en invente pas."
    
    return facts


def research_topic(topic: str) -> str:
    """
    Fonction principale : recherche + extraction des faits.
    Retourne un contexte factuel prêt à injecter dans le prompt.
    """
    
    print(f"🔍 Recherche en cours sur : {topic}")
    
    # Deux recherches complémentaires
    results_fr = search_web(f"{topic} statistiques étude 2024 2025", num_results=3)
    results_en = search_web(f"{topic} statistics report 2024 2025", num_results=3)
    
    all_results = results_fr + results_en
    
    if all_results:
        print(f"✅ {len(all_results)} sources trouvées")
    else:
        print("⚠️  Aucune source — le post sera généré sans statistiques externes")
    
    return extract_facts(topic, all_results)