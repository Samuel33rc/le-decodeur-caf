import streamlit as st
import json
import os

# Configuration de la page
st.set_page_config(page_title="Le Décodeur CAF", page_icon="📄")

# Styles personnalisés pour une UI plus "pro"
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
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Le Décodeur CAF")
st.subheader("Traduisez vos courriers CAF en actions concrètes (Gratuit & Privé)")

st.info("""
**Comment ça marche ?**
1. **Collez** votre courrier ci-dessous.
2. **Copiez** le "Prompt Expert" généré.
3. **Envoyez-le** à votre IA habituelle (ChatGPT, Gemini, etc.).
4. **Récupérez** votre rapport clair et actionnable.
""")

# ÉTAPE 1 : Saisie du texte
text_input = st.text_area("✍️ 1. Copiez-collez le texte de votre courrier CAF ici :", height=200, placeholder="Ex: Nous avons procédé au calcul de vos droits...")

if text_input:
    st.markdown("---")
    st.write("### 🤖 2. Votre Prompt Expert est prêt !")
    st.write("Cliquez sur l'icône de copie en haut à droite du cadre ci-dessous, puis collez-le dans votre IA (ChatGPT/Gemini).")
    
    # Construction du prompt optimisé
    full_prompt = f"""
Tu es un expert en administration française, spécialisé dans la CAF. 
Ton rôle est de traduire ce courrier complexe en langage simple et bienveillant.

CONTEXTE DU COURRIER :
{text_input}

CONSIGNES :
1. Résume l'essentiel en une phrase simple.
2. Explique clairement l'impact sur le budget (gain, perte, dette).
3. Liste les 3 prochaines étapes concrètes à faire.
4. Explique les 2 ou 3 termes techniques les plus complexes.

RÉPONDS EXACTEMENT SELON CE FORMAT :
### 💡 Ce que ça veut dire en 1 phrase
[Ta réponse ici]

### 💰 Impact sur votre argent
[Ta réponse ici]

### ✅ Ce que vous devez faire (Actions)
* [Action 1]
* [Action 2]
* [Action 3]

### 📚 Le jargon expliqué
* [Terme] : [Définition simple]
"""
    # Utilisation de st.code pour le bouton de copie natif
    st.code(full_prompt, language="markdown")

    st.markdown("---")
    # ÉTAPE 2 : Récupération du résultat
    st.write("### 🔍 3. Une fois analysé, collez le résultat ici :")
    agent_output = st.text_area("Collez la réponse de l'IA ici pour finaliser votre rapport :", height=200)

    if agent_output:
        st.success("✅ Rapport généré avec succès !")
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(agent_output)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ÉTAPE 3 : Export
        st.download_button(
            label="📥 Télécharger mon rapport (TXT)",
            data=agent_output,
            file_name="mon_rapport_decodeur_caf.txt",
            mime="text/plain"
        )

# --- ANALYTICS (GoatCounter) ---
# Remplace 'decodeur-caf' par ton identifiant GoatCounter réel si différent
st.components.v1.html(
    """
    <script data-goatcounter="https://decodeur-caf.goatcounter.com/count"
            async src="//gc.zgo.at/count.js"></script>
    """,
    height=0,
)

st.divider()

# Section Confiance & Local-First
with st.expander("🛡️ Sécurité & Vie Privée (Local-First)"):
    st.write("""
    **Votre vie privée est notre priorité :**
    - **Aucune base de données** : Nous ne stockons pas vos courriers. L'analyse est éphémère.
    - **Anonymisation conseillée** : Nous vous encourageons à supprimer vos noms/adresses avant copie.
    - **Contrôle total** : C'est vous qui envoyez le prompt à l'IA de votre choix (ChatGPT, Gemini, etc.).
    - **Zéro Budget** : Ce projet est une initiative citoyenne et solidaire.
    """)

st.caption("Le Décodeur CAF | Outil de solidarité numérique | Zéro Budget | Respect de la vie privée")
