import json
from openai import OpenAI
from config import OPENAI_API_KEY, YOUR_NICHE, YOUR_LANGUAGE, YOUR_TONE, TARGET_AUDIENCE
from prompts import SYSTEM_PROMPT, post_prompt

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_post(topic: str) -> dict:
    """Génère un post LinkedIn avec recherche web intégrée."""
    
    from researcher import research_topic
    from prompts import post_prompt
    
    print(f"\n🤖 Génération du post sur : {topic}")
    print("=" * 50)
    
    # Recherche des faits réels
    facts = research_topic(topic)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": post_prompt(topic, facts)}
        ],
        temperature=0.8,
        max_tokens=800
    )
    
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    result = json.loads(raw)
    return result

def display_post(result: dict, topic: str):
    """Affiche le post de manière lisible."""
    
    print(f"\n🎯 SUJET : {topic}")
    print("-" * 50)
    print(f"🪝 HOOK : {result['hook']}")
    print("-" * 50)
    print(f"\n📝 POST COMPLET :\n")
    print(result['post'])
    print("-" * 50)
    hashtags = " ".join([f"#{h}" for h in result['hashtags']])
    print(f"\n🏷️  HASHTAGS : {hashtags}")
    print(f"📊 SCORE VIRAL : {result['score_viral']}/10")
    if "pourquoi_ca_marche" in result:
        print(f"🧠 ANGLE : {result['pourquoi_ca_marche']}")
    print("=" * 50)

def run():
    """Boucle principale de l'agent."""
    
    print("\n🚀 AGENT LINKEDIN — IA & CYBERSÉCURITÉ")
    print(f"🎯 Niche : {YOUR_NICHE}")
    print(f"👥 Audience : {TARGET_AUDIENCE}")
    print("\nTape 'quit' pour quitter.\n")
    
    while True:
        topic = input("💡 Donne-moi un sujet : ").strip()
        
        if topic.lower() == 'quit':
            print("\n👋 Agent arrêté.")
            break
            
        if not topic:
            print("⚠️  Sujet vide, réessaie.")
            continue
        
        try:
            result = generate_post(topic)
            display_post(result, topic)
            
            # Sauvegarder le post
            save = input("\n💾 Sauvegarder ce post ? (o/n) : ").strip().lower()
            if save == 'o':
                save_post(result, topic)
                
        except json.JSONDecodeError:
            print("❌ Erreur de format JSON — relance ou change le sujet.")
        except Exception as e:
            print(f"❌ Erreur : {e}")

def save_post(result: dict, topic: str):
    """Sauvegarde le post dans un fichier texte."""
    import os
    from datetime import datetime
    
    os.makedirs("posts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"posts/post_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"SUJET: {topic}\n")
        f.write(f"DATE: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(result['post'])
        f.write(f"\n\n---\n")
        hashtags = " ".join([f"#{h}" for h in result['hashtags']])
        f.write(f"{hashtags}\n")
    
    print(f"✅ Post sauvegardé : {filename}")

if __name__ == "__main__":
    run()