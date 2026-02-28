# VISION.md - Vision du Produit X : Le Décodeur CAF (Local-First)

## Objectif en 1 phrase
Un "décodeur" de jargon administratif local et privé qui transforme les courriers et interfaces complexes de la CAF en actions claires et compréhensibles.

## Utilisateur cible
Bénéficiaires de la CAF (RSA, APL, AAH) souffrant de "phobie administrative" ou de difficultés de compréhension face au langage bureaucratique.

## MVP en 3 features max
1. **Analyseur de Documents Local** : Upload de PDF/Scan de courrier CAF traité 100% localement (via LLM local ou API avec anonymisation).
2. **Expliqueur de "Pourquoi ?"** : Traduction du jargon (ex: "Indu", "Quotient Familial") en langage courant avec l'impact concret sur le portefeuille.
3. **Checklist d'Actions** : Extraction automatique des pièces manquantes ou des démarches à faire sous forme de liste de tâches simple.

## Mesure de succès
- Temps de compréhension d'un courrier réduit de 10 min à 1 min.
- 100% des données restent sur la machine de l'utilisateur (Zéro fuite).
- Validation de l'utilité par 5 utilisateurs tests via Reddit.

## Différenciation
Contrairement aux forums ou aides sociales classiques, c'est **instantané, privé (Local-First) et disponible 24/7**.

## Plan d'Orchestration Simple
1. **Étape 1 (UI Locale)** : Créer une interface Streamlit simple pour l'upload (Skill: prototype-mvp).
2. **Étape 2 (Intelligence)** : Intégrer un prompt système "Expert Administratif" (Skill: orchestrate).
3. **Étape 3 (Test)** : Tester avec un exemple de courrier anonymisé trouvé sur Reddit.
