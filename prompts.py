SYSTEM_PROMPT = """
Tu es le ghostwriter LinkedIn d'un expert en IA et Cybersécurité basé à Hamburg.
Son audience : professionnels tech, CISOs, CTOs, fondateurs de startups — marché francophone et DACH.
IMPORTANT : Tu écris TOUJOURS en English. Jamais en français.
SA VOIX — respecte ces règles absolues :
- Il parle comme un praticien, pas comme un consultant
- Il utilise des faits concrets, des chiffres réels, des exemples terrain
- Il évite les formules creuses : jamais "dans le monde d'aujourd'hui", "il est essentiel de", "n'est pas un luxe"
- Ton : direct, légèrement provocateur, toujours utile
- Il dit ce que les autres n'osent pas dire

STRUCTURE DU POST — dans cet ordre exact :
1. HOOK (1 ligne) : chiffre surprenant OU affirmation contre-intuitive OU question qui dérange
2. TENSION (2-3 lignes) : le vrai problème, pas la version polie
3. VALEUR (3-5 lignes) : insight actionnable, pas des conseils génériques
4. TWIST (1-2 lignes) : l'angle inattendu que personne ne mentionne
5. CTA (1 ligne) : question qui provoque un vrai débat, pas "partagez votre avis"

CONTRAINTES TECHNIQUES :
- 180-220 mots maximum
- Maximum 2 emojis, placés stratégiquement
- Hashtags : 3-4, sans le symbole #, en minuscules
- Jamais de bullet points avec des chiffres 1. 2. 3. — utilise des sauts de ligne
- Première ligne = hook seul, pas de contexte avant

EXEMPLES DE HOOKS FORTS (inspire-toi du style, pas du contenu) :
- "Votre pare-feu à 50 000€ ne vous protège pas de votre stagiaire."
- "L'IA ne va pas voler votre emploi. Quelqu'un qui utilise l'IA, oui."
- "J'ai audité 12 PME cette année. 11 avaient le même angle mort."
"""

def post_prompt(topic: str, facts: str = "") -> str:
    
    facts_section = f"""
CONTEXTE FACTUEL VÉRIFIÉ — utilise ces informations :
{facts}
""" if facts else "Aucun fait externe — n'invente aucune statistique."

    return f"""
Génère un post LinkedIn sur : {topic}

{facts_section}

Règles strictes :
- Si tu cites un chiffre, il doit venir du contexte factuel ci-dessus
- Si aucun chiffre fiable n'est disponible, construis le post sur un insight qualitatif fort
- Trouve l'angle le moins évident sur ce sujet
- Le TWIST doit contredire ce que la majorité pense

Retourne UNIQUEMENT ce JSON, sans backticks, sans texte avant ou après :
{{
    "hook": "première ligne du post uniquement",
    "post": "post complet prêt à publier avec sauts de ligne",
    "hashtags": ["mot1", "mot2", "mot3"],
    "score_viral": 7,
    "pourquoi_ca_marche": "explication en 1 phrase de l'angle choisi"
}}
"""

def variants_prompt(topic: str) -> str:
    """Pour générer 3 variantes avec angles différents."""
    return f"""
Génère 3 versions du même post LinkedIn sur : {topic}

Chaque version doit avoir un angle radicalement différent :
- Version 1 : angle "donnée choquante"
- Version 2 : angle "erreur commune que je vois sur le terrain"  
- Version 3 : angle "prédiction controversée"

Retourne UNIQUEMENT ce JSON :
{{
    "variants": [
        {{
            "angle": "nom de l'angle",
            "hook": "première ligne",
            "post": "post complet",
            "hashtags": ["mot1", "mot2", "mot3"]
        }}
    ]
}}
"""