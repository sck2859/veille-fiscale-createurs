import os
from google import genai

# 1. Connexion sécurisée à l'API Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY est introuvable. Pense à l'ajouter dans les Settings de GitHub.")

client = genai.Client(api_key=api_key)

# 2. Fonction magique pour générer les blocs HTML sans découpage de texte fragile
def generer_flux_veille(theme_recherche, specifications):
    consigne = f"""
    Tu es un robot de veille juridique automatisé en droit fiscal français. Ton but est d'aider une étudiante en Master.
    Recherche et génère les 3 actualités réelles ou jurisprudences les plus marquantes et récentes (jusqu'en 2026) concernant ce thème précis : {theme_recherche}.
    Prends en compte ces spécifications pour cibler les sources : {specifications}.

    Pour chaque actualité, génère STRICTEMENT ce bloc HTML (et rien d'autre) :
    <div class="veille-item" style="background: white; padding: 1rem; margin-bottom: 0.8rem; border-radius: 6px; border-left: 4px solid #c5a059; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <span style="font-size: 0.8rem; font-weight: bold; color: #718096; text-transform: uppercase;">[NOM_DE_LA_SOURCE_OFFICIELLE]</span>
        <p style="margin: 0.3rem 0; font-weight: 500; color: #2d3748;">TITRE_DE_L_ACTUALITE_OU_ARRET_JURIDIQUE</p>
        <a href="LIEN_VERS_LE_SITE_OFFICIEL" target="_blank" style="font-size: 0.85rem; color: #c5a059; text-decoration: none; font-weight: bold;">→ Accéder à la source officielle</a>
    </div>

    Règle absolue : Renvoie uniquement le code HTML des blocs collés les uns après les autres. Ne mets aucun commentaire, aucun blabla d'introduction, et pas de balises de code Markdown du type ```html.
    """
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=consigne)
        clean_text = response.text.replace("```html", "").replace("```", "").strip()
        return clean_text
    except Exception as e:
        print(f"Erreur lors de la génération pour {theme_recherche} : {e}")
        return ""

try:
    print("Début de la collecte de la veille fiscale...")

    # 3. Lancement des 4 requêtes ciblées à l'IA
    print("- Collecte des actualités sur les Influenceurs (Sujet Mémoire)...")
    flux_memoire = generer_flux_veille(
        "Régime fiscal des influenceurs et créateurs de contenu", 
        "Cible tout ce qui concerne l'imposition des plateformes (OnlyFans, Patreon), les créateurs de contenu à l'étranger et la requalification des cadeaux/avantages en nature."
    )

    print("- Collecte de la Jurisprudence...")
    flux_jurisprudence = generer_flux_veille(
        "Jurisprudence fiscale (Conseil d'État, CJUE, Cour de cassation)", 
        "Cible les arrêts récents sur l'économie numérique, les plateformes en ligne et la territorialité de la TVA."
    )

    print("- Collecte de la Doctrine Administrative...")
    flux_bofip = generer_flux_veille(
        "Doctrine administrative et textes officiels (BOFiP, Légifrance)", 
        "Cible les publications officielles du BOFiP sur le régime des micro-BNC, le prélèvement à la source ou la TVA des services numériques."
    )

    print("- Collecte de la Doctrine Universitaire...")
    flux_doctrine = generer_flux_veille(
        "Doctrine universitaire et revues juridiques (Dalloz, Navis Francis Lefebvre, Lextenso)", 
        "Cible les articles de doctrine majeurs, les analyses d'avocats et les chroniques de revues fiscales."
    )

    # 4. Lecture du fichier index.html d'origine
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 5. Injection dynamique par ID (Méthode IT Toolkit nettoyée et sécurisée)
    # On découpe à l'ouverture de la balise, on jette l'ancien contenu et on remet le nouveau
    if '<div id="memoire-container">' in html:
        avant, apres = html.split('<div id="memoire-container">', 1)
        ancien_contenu, reste = apres.split('</div>', 1)
        html = f"{avant}<div id=\"memoire-container\">\n{flux_memoire}\n</div>{reste}"

    if '<div id="jurisprudence-container">' in html:
        avant, apres = html.split('<div id="jurisprudence-container">', 1)
        ancien_contenu, reste = apres.split('</div>', 1)
        html = f"{avant}<div id=\"jurisprudence-container\">\n{flux_jurisprudence}\n</div>{reste}"

    if '<div id="bofip-container">' in html:
        avant, apres = html.split('<div id="bofip-container">', 1)
        ancien_contenu, reste = apres.split('</div>', 1)
        html = f"{avant}<div id=\"bofip-container\">\n{flux_bofip}\n</div>{reste}"

    if '<div id="doctrine-container">' in html:
        avant, apres = html.split('<div id="doctrine-container">', 1)
        ancien_contenu, reste = apres.split('</div>', 1)
        html = f"{avant}<div id=\"doctrine-container\">\n{flux_doctrine}\n</div>{reste}"

    # 6. Sauvegarde finale
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Veille fiscale rafraîchie avec succès et injectée sans aucun bug !")

except Exception as e:
    print(f"Erreur générale lors de l'exécution : {e}")
    raise e
