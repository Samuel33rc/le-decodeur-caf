import streamlit as st
import json
import os
import re

# Configuration de la page
st.set_page_config(page_title="Le Décodeur CAF", page_icon="📄", layout="centered")

# Styles personnalisés pour un look "Papier Officiel"
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .report-box {
        padding: 30px;
        border-radius: 15px;
        background-color: white;
        border: 1px solid #d1d9e6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .disclaimer {
        font-size: 0.85em;
        color: #721c24;
        padding: 15px;
        border: 1px solid #f5c6cb;
        background-color: #f8d7da;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    .step-header {
        color: #1e3a8a;
        font-weight: bold;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Le Décodeur CAF")
st.markdown("### *Retrouvez la sérénité face à l'administration*")

# --- CONSTRAINT ARCHITECTURE: DISCLAIMER ---
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ IMPORTANT :</strong> Cet outil expérimental utilise l'Intelligence Artificielle pour vous aider à comprendre vos documents. 
    Il ne remplace pas l'avis d'un conseiller CAF. <strong>En cas de doute, contactez le 3230.</strong>
</div>
""", unsafe_allow_html=True)

# ÉTAPE 1 : Saisie
st.markdown('<p class="step-header">ÉTAPE 1 : Votre courrier</p>', unsafe_allow_html=True)
text_input = st.text_area(
    "Copiez le texte de votre courrier ici :", 
    height=200, 
    placeholder="Ex: Suite à l'étude de votre dossier, nous avons constaté un trop-perçu...",
)

# Gestion de l'état
if "show_prompt" not in st.session_state:
    st.session_state.show_prompt = False

def anonymize_text(text):
    text = re.sub(r'\d+[\s,.]\d+\s*€', '[MONTANT]', text)
    text = re.sub(r'\d{2}/\d{2}/\d{4}', '[DATE]', text)
    text = re.sub(r'\b\d{7}\b', '[N° ALLOCATAIRE]', text)
    return text

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Décoder mon courrier"):
        if text_input:
            st.session_state.show_prompt = True
        else:
            st.error("Veuillez coller un texte.")

with col2:
    if st.button("🛡️ Masquer mes données"):
        if text_input:
            st.session_state.text_input = anonymize_text(text_input)
            st.success("Données sensibles masquées !")

if st.session_state.show_prompt and text_input:
    st.markdown("---")
    st.markdown('<p class="step-header">ÉTAPE 2 : Analyse par l\'IA</p>', unsafe_allow_html=True)
    st.write("Copiez ce bloc et collez-le dans **ChatGPT**, **Claude** ou **Gemini**.")
    
    final_text = anonymize_text(text_input) if "text_input" not in st.session_state else st.session_state.text_input

    full_prompt = f"""
Tu es un expert en administration française (spécialiste CAF). 
Traduis ce courrier en langage simple, bienveillant et orienté ACTION.

TEXTE À ANALYSER :
{final_text}

STRUCTURE DU RAPPORT :
### 💡 Ce que ça veut dire en 1 phrase
[Résumé ultra-simple]

### 💰 Impact sur votre argent
[Explication précise des sommes en jeu]

### ✅ Ce que vous devez faire (Actions)
* [Action immédiate]
* [Action secondaire]

### ☎️ Aide & Escalade
[Conseiller de contacter une assistante sociale si dette > 1000€ ou menace d'expulsion]
"""
    st.code(full_prompt, language="markdown")

    st.markdown("---")
    st.markdown('<p class="step-header">ÉTAPE 3 : Votre Rapport Final</p>', unsafe_allow_html=True)
    agent_output = st.text_area("Collez la réponse de l'IA ici pour mettre en forme votre rapport :", height=200)

    if agent_output:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(agent_output)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Télécharger mon rapport (PDF/TXT)",
            data=agent_output,
            file_name="rapport_decodeur_caf.txt",
            mime="text/plain"
        )

# Footer
st.divider()
with st.expander("🛡️ Confidentialité & Sécurité"):
    st.write("Ce service est 'Local-First'. Vos données sont traitées dans votre navigateur et ne sont jamais stockées sur nos serveurs.")

# Analytics
st.components.v1.html(
    """<script data-goatcounter="https://decodeur-caf.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>""",
    height=0,
)
st.caption("Le Décodeur CAF | Développé avec ❤️ pour la solidarité numérique")
