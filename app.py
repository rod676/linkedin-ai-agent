import json
import streamlit as st
from agent import generate_post, save_post
from config import YOUR_NICHE, TARGET_AUDIENCE

st.set_page_config(
    page_title="LinkedIn AI Agent",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 LinkedIn Content Agent")
st.caption(f"Niche : {YOUR_NICHE} · Audience : {TARGET_AUDIENCE}")
st.divider()

topic = st.text_input(
    "💡 Sujet du post",
    placeholder="Ex: Les attaques ransomware contre les PME en 2025"
)

col1, col2 = st.columns([1, 3])
with col1:
    generate_btn = st.button("Générer", type="primary", use_container_width=True)

if generate_btn and topic:
    with st.spinner("🔍 Recherche web + génération en cours..."):
        try:
            result = generate_post(topic)

            st.subheader("🪝 Hook")
            st.info(result.get("hook", "Pas de hook généré."))

            st.subheader("📝 Post complet")
            post_area = st.text_area(
                label="",
                value=result.get("post", ""),
                height=300,
                label_visibility="collapsed"
            )

            hashtags = " ".join([f"#{h}" for h in result.get("hashtags", [])])
            if hashtags:
                st.caption(f"🏷️ {hashtags}")

            st.code(result.get("post", "") + (f"\n\n{hashtags}" if hashtags else ""), language=None)
            st.caption("☝️ Copie ce bloc directement dans LinkedIn")

            if "pourquoi_ca_marche" in result:
                with st.expander("🧠 Pourquoi cet angle fonctionne"):
                    st.write(result["pourquoi_ca_marche"])

            if st.button("💾 Sauvegarder ce post"):
                save_post(result, topic)
                st.success("✅ Post sauvegardé dans /posts")

        except json.JSONDecodeError:
            st.error("❌ Erreur de format — réessaie ou change le sujet.")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")

elif generate_btn and not topic:
    st.warning("⚠️ Entre un sujet avant de générer.")

st.divider()
st.caption("Built with OpenAI + Serper · Hamburg 🇩🇪")
