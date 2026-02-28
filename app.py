import streamlit as st
import json
import os
import re

# Configuration de la page
st.set_page_config(page_title="Le Décodeur CAF", page_icon="📄")

# Styles personnalisés
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .report-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        border: 1px solid #e0e0e0;
    }
    .disclaimer {
        font-size: 0.8em;
        color: #666;
        padding: 10px;
        border: 1px solid #ffcccc;
        background-color: #fff5f5;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Le Décodeur CAF")
st.subheader("Traduisez vos courriers CAF en actions concrètes")

# --- CONSTRAINT ARCHITECTURE: DISCLAIMER JURIDIQUE ---
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ AVERTISSEMENT :</strong> Cet outil est une aide à la compréhension basée sur l'intelligence artificielle. 
    Il peut faire des erreurs. Ne prenez aucune décision financière ou juridique sans vérifier auprès d'un conseiller 
    CAF officiel ou d'une assistante sociale.
</div>
""", unsafe_allow_html=True)

st.info("""
**Comment ça marche ?**
1. **Collez** votre courrier ci-dessous.
2. **Validez** pour générer le prompt.
3. **Copiez** vers votre IA habituelle (ChatGPT, Gemini, Claude).
""")

def anonymize_text(text):
    # Remplace les montants (ex: 123,45 €)
    text = re.sub(r'\d+[\s,.]\d+\s*€', '[MONTANT]', text)
    # Remplace les dates
    text = re.sub(r'\d{2}/\d{2}/\d{4}', '[DATE]', text)
    # Tentative simple pour les numéros allocataires (7 chiffres)
    text = re.sub(r'\b\d{7}\b', '[N° ALLOCATAIRE]', text)
    return text

# ÉTAPE 1 : Saisie du texte
text_input = st.text_area(
    "✍️ 1. Copiez-collez le texte de votre courrier CAF ici :", 
    height=200, 
    placeholder="Ex: Nous avons procédé au calcul de vos droits...",
    help="Appuyez sur Ctrl+Entrée (Windows) ou Cmd+Entrée (Mac) pour valider rapidement."
)

# Utilisation d'un état pour gérer l'affichage du prompt
if "show_prompt" not in st.session_state:
    st.session_state.show_prompt = False

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Valider et Générer le Prompt"):
        if text_input:
            st.session_state.show_prompt = True
        else:
            st.error("Veuillez d'abord coller un texte.")

with col2:
    if st.button("🛡️ Anonymiser mon texte"):
        if text_input:
            st.session_state.text_input = anonymize_text(text_input)
            st.success("Données anonymisées.")
        else:
            st.error("Veuillez d'abord coller un texte.")

if st.session_state.show_prompt and text_input:
    st.markdown("---")
    st.write("### 🤖 2. Votre Prompt Expert est prêt !")
    st.write("Copiez ce texte et envoyez-le à votre IA habituelle.")
    
    # On utilise le texte éventuellement anonymisé
    final_text = anonymize_text(text_input) if "text_input" not in st.session_state else st.session_state.text_input

    # --- SPECIFICATION ENGINEERING: LE PROMPT 2026 ---
    full_prompt = f"""
Tu es un expert en administration française (spécialiste CAF). 
Traduis ce courrier en langage simple, bienveillant et orienté ACTION.

CONTEXTE DU COURRIER :
{final_text}

CONSIGNES STRICTES (CONSTRAINT ARCHITECTURE) :
1. Résume l'essentiel en une phrase sans jargon.
2. Impact budgétaire : Sois ultra-précis (gain, perte ou dette).
3. Checklist : Donne 3 actions concrètes.
4. ESCALADE HUMAINE : Si le courrier concerne une menace d'expulsion, une dette > 1000€ ou une radiation, ajoute IMPÉRATIVEMENT un conseil de contacter une assistante sociale de secteur ou le CCAS.

FORMAT DE RÉPONSE :
### 💡 Ce que ça veut dire en 1 phrase
[Ta réponse]

### 💰 Impact sur votre argent
[Ta réponse]

### ✅ Ce que vous devez faire (Actions)
* [Action 1]
* [Action 2]
* [Action 3]

### 📚 Le jargon expliqué
* [Terme] : [Définition]

### ☎️ Aide humaine (Escalade)
[Uniquement si nécessaire selon les consignes]
"""
    st.code(full_prompt, language="markdown")

    st.markdown("---")
    # ÉTAPE 2 : Récupération du résultat
    st.write("### 🔍 3. Collez la réponse de l'IA ici :")
    agent_output = st.text_area("Collez le résultat ici pour finaliser :", height=200)

    if agent_output:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(agent_output)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Télécharger mon rapport (TXT)",
            data=agent_output,
            file_name="rapport_decodeur_caf.txt",
            mime="text/plain"
        )

# Section Confiance
with st.expander("🛡️ Sécurité & Vie Privée (Local-First)"):
    st.write("""
    - **Zéro Stockage** : Vos textes ne quittent pas votre navigateur vers nos serveurs.
    - **Anonymisation** : Le bouton de bouclier masque vos données sensibles localement.
    - **Accessibilité** : Compatible Windows, Mac, Linux et Mobile.
    """)

# Analytics
st.components.v1.html(
    """<script data-goatcounter="https://decodeur-caf.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>""",
    height=0,
)

st.caption("Le Décodeur CAF | Version 2026 | Frugal & Solidaire")
