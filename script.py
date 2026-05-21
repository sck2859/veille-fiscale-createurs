import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : Clé GEMINI_API_KEY introuvable.")

client = genai.Client(api_key=api_key)

# Matière brute
base_donnees = """
- Source: [BOFiP]. Régime des micro-BNC et créateurs de contenu. Clarification sur l'articulation entre l'abattement de 34% et les dépenses réelles des influenceurs.
- Source: [Conseil d'État]. Arrêt CE, 15 mars 2026. Les gains issus d'abonnements directs étrangers (OnlyFans, Patreon) sont des BNC professionnels imposables en France.
- Source: [CJUE]. Territorialité de la TVA sur les services numériques. Détermination de la TVA pour les placements de produits transfrontaliers.
- Source: [Dalloz]. La requalification fiscale des avantages en nature (cadeaux, voyages) accordés aux influenceurs au titre de l'article 79 du CGI.
- Source: [Navis]. Structuration en SASU ou Entreprise Individuelle pour les streamers : arbitrage fiscal IR vs IS.
"""

consigne_ia = f"""
Tu es un avocat fiscaliste. Prends ces éléments : {base_donnees}.
Génère pour CHAQUE élément une carte HTML stricte au format suivant :

<div class="card">
    <div class="meta"><span>Source : NOM_DE_LA_SOURCE</span><span>Statut : Fiche de Synthèse</span></div>
    <h3>TITRE_DE_L_ARTICLE</h3>
    <p><b>Résumé de la position :</b> RESUME_JURIDIQUE_DE_L_IA</p>
    <p style="margin-top:0.5rem; font-size:0.9rem; color:#c5a059;"><b>💡 Intérêt pour le mémoire :</b> CONSEIL_DE_REDACTION_POUR_L_ETUDIANTE</p>
</div>

Règles de tri impératives :
- Si l'élément concerne le Conseil d'État ou la CJUE, mets la carte sous la ligne : - Si l'élément concerne le BOFiP ou Légifrance, mets la carte sous la ligne : - Si l'élément concerne Dalloz ou Navis, mets la carte sous la ligne : Renvoie uniquement le code contenant ces commentaires et les cartes correspondantes en dessous d'eux. Pas de balise ```html.
"""

try:
    response = client.models.generate_content(model='gemini-2.5-flash', contents=consigne_ia)
    resultat_ia = response.text

    # Tri basique et injection dans index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Dispatching simple des textes générés par l'IA dans les conteneurs
    # Pour s'assurer que tout s'affiche, on remplace les zones d'attente
    html = html.replace("", resultat_ia)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Injection réussie !")
except Exception as e:
    print(f"Erreur : {e}")
