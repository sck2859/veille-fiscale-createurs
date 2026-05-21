import os
from google import genai

# 1. Le script va chercher la clé API Gemini cachée en toute sécurité dans GitHub
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY n'est pas configurée dans les Secrets GitHub.")

client = genai.Client(api_key=api_key)

# 2. La base de données brute de départ pour le mémoire de ton amie
actualites_brutes = """
1. BOFiP (Doctrine Administrative) : Précisions sur le régime du micro-BNC applicable aux revenus publicitaires, commissions d'affiliation et abonnements des créateurs de contenu (Twitch, YouTube).
2. Conseil d'État (Jurisprudence) : Arrêt majeur qualifiant les gains réguliers d'un vidéaste sur une plateforme étrangère comme bénéfices professionnels imposables en France.
3. CJUE (Droit Européen) : Analyse de l'assujettissement à la TVA des services numériques fournis par les créateurs à des abonnés résidant en dehors de l'Union Européenne.
4. Doctrine (Dalloz, Navis, Lextenso) : Étude doctrinale sur le risque de redressement fiscal lié aux cadeaux et avantages en nature (vêtements, voyages gratuits) non déclarés par les influenceurs.
5. Légifrance : Suivi du projet de loi visant à renforcer le contrôle fiscal et la transparence des revenus issus des plateformes d'abonnements directs (OnlyFans, MYM).
"""

# 3. Consignes ultra-précises à l'IA pour générer les fiches de veille pour le mémoire
consigne_ia = f"""
Tu es un avocat fiscaliste expert de l'économie numérique. Tu dois aider une étudiante à structurer sa veille pour son mémoire sur "Le régime fiscal des créateurs de contenu".
Prends les actualités brutes suivantes et transforme-les en une série de fiches de veille universitaire haut de gamme au format HTML.

Actualités à traiter :
{actualites_brutes}

Consignes impératives pour chaque fiche :
- Rédige une structure sous forme de bloc <div class="card">...</div> pour chaque actualité (sans refaire toute la page, juste les cartes).
- Donne un titre clair axé sur la fiscalité des créateurs.
- Identifie la source exacte (BOFiP, Conseil d'État, CJUE, Dalloz, Navis, Légifrance).
- Rédige un "Résumé Analytique" rigoureux en langage juridique.
- Rédige une section "Impact pour le Mémoire" qui explique concrètement ce que cela apporte à son argumentation ou ses parties de mémoire.
- Ajoute une liste de mots-clés.

Renvoie UNIQUEMENT le code HTML des blocs <div class="card">...</div> les uns après les autres. N'inclus aucune balise de code comme ```html au début ou à la fin.
"""

print("Lancement de l'IA Gemini pour la synthèse juridique...")

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=consigne_ia
    )
    
    html_fiches = response.text
    
    # 4. On ouvre le fichier index.html d'origine pour y injecter les fiches de l'IA
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        
    # On repère la zone d'injection grâce à la balise de notre squelette
    start_tag = '<main class="feed" id="veille-content">'
    end_tag = '</main>'
    
    parts = html_content.split(start_tag)
    subparts = parts[1].split(end_tag)
    
    # Reconstitution propre du site avec le contenu actualisé par l'IA
    nouveau_html = parts[0] + start_tag + "\n" + html_fiches + "\n" + end_tag + subparts[1]
    
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(nouveau_html)
        
    print("Succès ! Les fiches d'analyse fiscale ont été injectées dans le site.")

except Exception as e:
    print(f"Une erreur est survenue lors du traitement : {e}")
