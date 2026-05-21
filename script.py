import os
from google import genai

# 1. Vérification et connexion à l'IA Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY n'est pas configurée dans les Secrets GitHub.")

client = genai.Client(api_key=api_key)

# 2. Base de données brute complète (Doctrine, Jurisprudence, BOFiP...)
base_donnees_fiscales = """
[SOURCE:BOFiP] [CATEGORIE:DOCTRINE_ADMINISTRATIVE]
Titre: Régime des micro-BNC et créateurs de contenu sur les plateformes de streaming
Contenu: Mise à jour de la doctrine administrative concernant l'articulation entre l'abattement forfaitaire de 34% et les dépenses réelles des influenceurs (frais de matériel, setup, serveurs). Clarification sur l'obligation de basculer au régime réel si les plateformes de monétisation (Twitch, YouTube) versent des redevances de droits d'auteur de manière prépondérante.

[SOURCE:Conseil d'État] [CATEGORIE:JURISPRUDENCE]
Titre: Arrêt CE, 15 mars 2026 - Qualification des revenus issus d'abonnements directs étrangers
Contenu: Le Conseil d'État statue sur le cas d'un créateur résidant en France percevant des revenus via des plateformes basées aux États-Unis et au Royaume-Uni (type OnlyFans, Patreon). Les gains sont qualifiés de bénéfices non commerciaux (BNC) professionnels dès lors que l'activité est exercée à titre habituel, entraînant l'application de la retenue à la source et le contrôle des flux financiers internationaux.

[SOURCE:CJUE] [CATEGORIE:JURISPRUDENCE]
Titre: Arrêt CJUE - Territorialité de la TVA sur les services numériques de divertissement
Contenu: Analyse de l'assujettissement à la TVA européenne pour les placements de produits et les sponsorings transfrontaliers. La Cour précise les critères de localisation du preneur de services et l'obligation d'immatriculation à la TVA dès le premier euro pour les prestations électroniques fournies à des consommateurs finaux (B2C) en dehors du pays d'établissement.

[SOURCE:Dalloz / Revue de Droit Fiscal] [CATEGORIE:DOCTRINE_UNIVERSITAIRE]
Titre: La requalification fiscale des avantages en nature accordés aux influenceurs
Contenu: Étude doctrinale approfondie sur l'article 79 du Code général des impôts (CGI). Les auteurs analysent le risque de redressement fiscal lorsque des créateurs de contenu omettent de déclarer la valeur marchande des cadeaux, vêtements de luxe, ou séjours à l'hôtel offerts par les marques en échange d'une visibilité. Recommandations pour l'évaluation de la valeur réelle de ces dotations.

[SOURCE:Navis / Editions Francis Lefebvre] [CATEGORIE:DOCTRINE_UNIVERSITAIRE]
Titre: Structuration sociétaire des créateurs de contenu : Arbitrage entre Entreprise Individuelle et SASU
Contenu: Analyse d'impact sur l'optimisation fiscale des revenus des streamers de grande taille. Comparaison des taux effectifs d'imposition entre l'impôt sur le revenu (IR) et l'impôt sur les sociétés (IS), et risques de requalification en abus de droit en cas de distribution disproportionnée de dividendes.

[SOURCE:Légifrance] [CATEGORIE:DOCTRINE_ADMINISTRATIVE]
Titre: Projet de Loi de Finances - Renforcement des contrôles sur l'économie des plateformes
Contenu: Suivi des amendements législatifs imposant aux plateformes numériques de transmettre automatiquement l'intégralité des volumes de transactions et d'abonnements au fisc français, harmonisant le contrôle de la fraude fiscale sur les revenus numériques.
"""

# 3. Consigne ultra-précise pour concevoir le gros Toolkit de mémoire
consigne_ia = f"""
Tu es un avocat fiscaliste de haut niveau et directeur de recherche en droit fiscal numérique. 
Tu dois générer un site web Toolkit intégral et parfaitement structuré en HTML pour un mémoire universitaire intitulé : "Le régime fiscal des créateurs de contenu".

Utilise ce code de structure HTML globale et injecte de manière très structurée les articles et analyses de doctrine/jurisprudence à l'intérieur des bonnes catégories :

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT & Tax Legal Toolkit - Mémoire de Recherche</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Tax Legal Toolkit</h1>
        <p>Espace de Recherche & Veille Analytique • Le régime fiscal des créateurs de contenu</p>
    </header>

    <div class="container">
        <aside class="sidebar">
            <h3>Structure du Mémoire</h3>
            <ul style="list-style: none; padding-left: 0; font-size: 0.9rem; line-height: 1.8;">
                <li>📁 <b>Partie I : La qualification des revenus</b></li>
                <li>└ ℹ️ BNC, Micro-BNC et Droits d'auteur</li>
                <li>📁 <b>Partie II : La fiscalité indirecte & internationale</b></li>
                <li>└ ℹ️ Territorialité de la TVA & Flux transfrontaliers</li>
            </ul>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 1.5rem 0;">
            <h3>Sources Analysées</h3>
            <div class="tags">
                <span class="tag">Conseil d'État</span>
                <span class="tag">CJUE</span>
                <span class="tag">BOFiP</span>
                <span class="tag">Légifrance</span>
                <span class="tag">Dalloz</span>
                <span class="tag">Navis</span>
            </div>
        </aside>

        <main class="feed">
            <section class="category-section">
                <h2 class="category-title">⚖️ 1. Jurisprudence & Contentieux (CE, Cass, CJUE)</h2>
                <div id="jurisprudence-container">
                    </div>
            </section>

            <section class="category-section" style="margin-top: 3rem;">
                <h2 class="category-title">📜 2. Doctrine Administrative & Textes (BOFiP, Lois)</h2>
                <div id="bofip-container">
                    </div>
            </section>

            <section class="category-section" style="margin-top: 3rem;">
                <h2 class="category-title">📚 3. Doctrine Universitaire & Revues (Dalloz, Navis, Lextenso)</h2>
                <div id="doctrine-container">
                    </div>
            </section>
        </main>
    </div>
</body>
</html>

Pour CHAQUE élément de la base de données brute {base_donnees_fiscales}, crée un bloc d'analyse complet structuré de la manière suivante (respecte scrupuleusement l'affectation dans le bon container) :

<div class="card">
    <div class="meta"><span>Source : NOM_DE_LA_SOURCE</span><span>Statut : Analyse Académique</span></div>
    <h3>TITRE_DE_L_ARTICLE</h3>
    <p><b>Résumé de l'article :</b> TEXTE_DU_RESUME_JURIDIQUE_DE_L_IA</p>
    <div style="background: #f7fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 6px; margin-top: 1rem;">
        <h4 style="margin: 0 0 0.5rem 0; color: #c5a059; font-size: 0.85rem; text-transform: uppercase;">💡 Apport pour le Mémoire</h4>
        <p style="margin: 0; font-size: 0.9rem; color: #4a5568;">EXPLICATION_PRECISE_POUR_REDACTION_DU_MEMOIRE</p>
    </div>
</div>

Renvoie UNIQUEMENT le code HTML final complet, sans aucune balise de code comme ```html au début ou à la fin. Remplace bien les commentaires d'injections par les vraies cartes générées et triées.
"""

print("Génération du Toolkit complet par l'IA Gemini...")

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=consigne_ia
    )
    
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response.text)
        
    print("🎉 Succès ! Le Toolkit de recherche complet a été généré dans index.html.")

except Exception as e:
    print(f"Erreur lors de la génération : {e}")
