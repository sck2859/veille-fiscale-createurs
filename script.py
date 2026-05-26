import os
from google import genai

# 1. Connexion à l'API Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY est introuvable.")

client = genai.Client(api_key=api_key)

# 2. Consigne pour l'IA
consigne_ia = """
Tu es un robot de veille juridique automatisé spécialisé en droit fiscal français.
Génère les dernières actualités réelles ou hautement probables pour l'année 2026 concernant la fiscalité des créateurs de contenu (influenceurs, streamers, OnlyFans).

Pour chaque actualité, crée un bloc HTML strict sous cette forme :
<div class="veille-item" style="background: white; padding: 1rem; margin-bottom: 0.8rem; border-radius: 6px; border-left: 4px solid #c5a059; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <span style="font-size: 0.8rem; font-weight: bold; color: #718096; text-transform: uppercase;">[NOM_DE_LA_SOURCE_OFFICIELLE]</span>
    <p style="margin: 0.3rem 0; font-weight: 500; color: #2d3748;">TITRE_DE_L_ACTUALITE_OU_ARRET_JURIDIQUE</p>
    <a href="LIEN_VERS_LE_SITE_OFFICIEL" target="_blank" style="font-size: 0.85rem; color: #c5a059; text-decoration: none; font-weight: bold;">→ Accéder à la source officielle</a>
</div>

Règles de tri impératives :
- Place les cartes "Régime fiscal des influenceurs" sous la ligne : === BLOC_MEMOIRE ===
- Place les arrêts (CE, CJUE) sous la ligne : === BLOC_JURISPRUDENCE ===
- Place les textes officiels (BOFiP) sous la ligne : === BLOC_BOFIP ===
- Place les articles de revues (Dalloz, Navis) sous la ligne : === BLOC_DOCTRINE ===

Renvoie uniquement les blocs séparés par ces lignes repères, sans aucun autre texte.
"""

try:
    print("Appel de l'IA...")
    response = client.models.generate_content(model='gemini-2.5-flash', contents=consigne_ia)
    resultat_ia = response.text

    # Nettoyage de sécurité
    resultat_ia = resultat_ia.replace("```html", "").replace("```", "").strip()

    # Découpage ultra-sécurisé (si une balise manque, on met du texte vide au lieu de faire planter le script)
    cartes_memoire = ""
    cartes_jurisprudence = ""
    cartes_bofip = ""
    cartes_doctrine = ""

    if "=== BLOC_MEMOIRE ===" in resultat_ia and "=== BLOC_JURISPRUDENCE ===" in resultat_ia:
        cartes_memoire = resultat_ia.split("=== BLOC_MEMOIRE ===")[1].split("=== BLOC_JURISPRUDENCE ===")[0].strip()
    
    if "=== BLOC_JURISPRUDENCE ===" in resultat_ia and "=== BLOC_BOFIP ===" in resultat_ia:
        cartes_jurisprudence = resultat_ia.split("=== BLOC_JURISPRUDENCE ===")[1].split("=== BLOC_BOFIP ===")[0].strip()
        
    if "=== BLOC_BOFIP ===" in resultat_ia and "=== BLOC_DOCTRINE ===" in resultat_ia:
        cartes_bofip = resultat_ia.split("=== BLOC_BOFIP ===")[1].split("=== BLOC_DOCTRINE ===")[0].strip()
        
    if "=== BLOC_DOCTRINE ===" in resultat_ia:
        cartes_doctrine = resultat_ia.split("=== BLOC_DOCTRINE ===")[1].strip()

    # Lecture du fichier index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Injection propre (on ne remplace que si la section existe)
    html = html.replace('<div id="memoire-container"></div>', f'<div id="memoire-container">\n{cartes_memoire}\n</div>')
    html = html.replace('<div id="jurisprudence-container"></div>', f'<div id="jurisprudence-container">\n{cartes_jurisprudence}\n</div>')
    html = html.replace('<div id="bofip-container"></div>', f'<div id="bofip-container">\n{cartes_bofip}\n</div>')
    html = html.replace('<div id="doctrine-container"></div>', f'<div id="doctrine-container">\n{cartes_doctrine}\n</div>')

    # Sauvegarde
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Script exécuté sans planter !")

except Exception as e:
    print(f"Erreur interceptée pour éviter le plantage : {e}")
