import os
from google import genai

# 1. Connexion sécurisée à l'API Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY est introuvable.")

client = genai.Client(api_key=api_key)

# 2. Données brutes de la veille fiscale
base_donnees = """
- Source: [BOFiP]. Régime des micro-BNC et créateurs de contenu. Clarification sur l'articulation entre l'abattement de 34% et les dépenses réelles des influenceurs.
- Source: [Conseil d'État]. Arrêt CE, 15 mars 2026. Les gains issus d'abonnements directs étrangers (OnlyFans, Patreon) sont des BNC professionnels imposables en France.
- Source: [CJUE]. Territorialité de la TVA sur les services numériques. Détermination de la TVA pour les placements de produits transfrontaliers.
- Source: [Dalloz]. La requalification fiscale des avantages en nature (cadeaux, voyages) accordés aux influenceurs au titre de l'article 79 du CGI.
- Source: [Navis]. Structuration en SASU ou Entreprise Individuelle pour les streamers : arbitrage fiscal IR vs IS.
"""

# 3. Consigne pour récupérer uniquement les cartes HTML triées par balises repères
consigne_ia = f"""
Tu es un assistant de recherche en droit fiscal. Base-toi sur ces éléments : {base_donnees}.
Génère pour CHAQUE élément une carte HTML au format suivant :

<div class="card">
    <div class="meta"><span>Source : NOM_DE_LA_SOURCE</span><span>Statut : Fiche de Synthèse</span></div>
    <h3>TITRE_DE_L_ARTICLE</h3>
    <p><b>Résumé de la position :</b> RESUME_JURIDIQUE_DE_L_IA</p>
    <p style="margin-top:0.5rem; font-size:0.9rem; color:#c5a059;"><b>💡 Intérêt pour le mémoire :</b> CONSEIL_DE_REDACTION_POUR_L_ETUDIANTE</p>
</div>

Règles de tri impératives :
Mets toutes les cartes du Conseil d'État et de la CJUE sous la ligne : === BLOC_JURISPRUDENCE ===
Mets la carte du BOFiP sous la ligne : === BLOC_BOFIP ===
Mets les cartes de Dalloz et Navis sous la ligne : === BLOC_DOCTRINE ===

Renvoie uniquement le texte contenant ces trois lignes repères et leurs cartes associées. Pas de balises de code Markdown comme ```html.
"""

try:
    print("Appel de Gemini...")
    response = client.models.generate_content(model='gemini-2.5-flash', contents=consigne_ia)
    resultat_ia = response.text

    # Découpage des blocs reçus de l'IA
    cartes_jurisprudence = resultat_ia.split("=== BLOC_JURISPRUDENCE ===")[1].split("=== BLOC_BOFIP ===")[0].strip()
    cartes_bofip = resultat_ia.split("=== BLOC_BOFIP ===")[1].split("=== BLOC_DOCTRINE ===")[0].strip()
    cartes_doctrine = resultat_ia.split("=== BLOC_DOCTRINE ===")[1].strip()

    # Lecture du fichier de structure index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Injection par remplacement d'identifiants (Ta méthode de l'application IT)
    html = html.replace('<div id="jurisprudence-container"></div>', f'<div id="jurisprudence-container">\n{cartes_jurisprudence}\n</div>')
    html = html.replace('<div id="bofip-container"></div>', f'<div id="bofip-container">\n{cartes_bofip}\n</div>')
    html = html.replace('<div id="doctrine-container"></div>', f'<div id="doctrine-container">\n{cartes_doctrine}\n</div>')

    # Sauvegarde du fichier final mis à jour
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Fiches injectées proprement avec ta méthode d'origine !")

except Exception as e:
    print(f"Erreur d'exécution : {e}")
    raise e
