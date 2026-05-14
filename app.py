import streamlit as st
import json
from datetime import datetime
from agent import generate_post
from carousel import generate_carousel_content, generate_carousel_pptx
from config import YOUR_NICHE, TARGET_AUDIENCE

st.set_page_config(
    page_title="LinkedIn AI Agent",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 LinkedIn AI Content Agent")
st.caption(f"Niche: {YOUR_NICHE} · Audience: {TARGET_AUDIENCE}")
st.divider()

tab1, tab2 = st.tabs(["📝 Text Post", "🎨 Carousel"])

# Tab 1 — Text Post (existant)
with tab1:
    topic = st.text_input(
        "💡 Post topic",
        placeholder="Ex: The biggest cybersecurity mistake SMEs make in 2025"
    )
    
    if st.button("Generate Post", type="primary"):
        if topic:
            with st.spinner("🔍 Researching + generating..."):
                try:
                    result = generate_post(topic)
                    
                    st.subheader("🪝 Hook")
                    st.info(result["hook"])
                    
                    st.subheader("📝 Full Post")
                    st.text_area(
                        label="",
                        value=result["post"],
                        height=300,
                        label_visibility="collapsed"
                    )
                    
                    hashtags = " ".join([f"#{h}" for h in result["hashtags"]])
                    st.caption(f"🏷️ {hashtags}")
                    
                    st.code(
                        result["post"] + f"\n\n{hashtags}",
                        language=None
                    )
                    st.caption("☝️ Copy this block directly into LinkedIn")
                    
                    if "pourquoi_ca_marche" in result:
                        with st.expander("🧠 Why this angle works"):
                            st.write(result["pourquoi_ca_marche"])
                    
                    if st.button("💾 Save post"):
                        from agent import save_post
                        save_post(result, topic)
                        st.success("✅ Saved in /posts")
                        
                except json.JSONDecodeError:
                    st.error("❌ Format error — try again or change topic.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please enter a topic")

# Tab 2 — Carousel (nouveau)
with tab2:
    carousel_topic = st.text_input(
        "🎨 Carousel topic",
        placeholder="Ex: 5 cybersecurity tools every developer must know",
        key="carousel_topic"
    )
    
    if st.button("Generate Carousel", type="primary", key="gen_carousel"):
        if carousel_topic:
            with st.spinner("🔍 Researching + building slides..."):
                try:
                    # Génère le contenu
                    carousel_data = generate_carousel_content(carousel_topic)
                    
                    # Preview des slides
                    st.subheader(f"📋 {carousel_data['title']}")
                    st.write(f"**{len(carousel_data['slides'])} slides generated**")
                    
                    for slide in carousel_data["slides"]:
                        with st.expander(
                            f"Slide {slide['slide_number']} "
                            f"{slide.get('emoji','')} — {slide['headline']}"
                        ):
                            st.write(slide.get("body", ""))
                    
                    with st.expander("🏁 CTA Slide"):
                        st.write(carousel_data.get("cta_text", ""))
                        st.write(carousel_data.get("author", ""))
                    
                    # Génère le PPTX
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = f"posts/carousel_{timestamp}.pptx"
                    
                    pptx_path = generate_carousel_pptx(
                        carousel_data,
                        output_path
                    )
                    
                    # Téléchargement
                    with open(pptx_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Carousel (PPTX)",
                            data=f,
                            file_name=f"carousel_{timestamp}.pptx",
                            mime="application/vnd.openxmlformats-officedocument"
                                  ".presentationml.presentation"
                        )
                    
                    st.success(
                        "✅ Carousel ready! Download PPTX → "
                        "Export as PDF in PowerPoint → "
                        "Upload to LinkedIn"
                    )
                    st.info(
                        "💡 In PowerPoint: File → Export → "
                        "Create PDF/XPS → Upload PDF to LinkedIn"
                    )
                    
                except json.JSONDecodeError:
                    st.error("❌ Format error — try again.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please enter a topic")

st.divider()
st.caption("Built with OpenAI + Serper · Hamburg 🇩🇪")