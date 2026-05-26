import os

# 1. Simulation de la collecte automatique des flux d'actualités fiscales (BOFiP, CE, Dalloz)
# Dans une version avancée, on viendrait lire les flux RSS de ces sites.
flux_actualites = [
    {
        "source": "Conseil d'État",
        "categorie": "jurisprudence",
        "titre": "Arrêt CE, 15 mars 2026 : Imposition des gains issus de plateformes étrangères (OnlyFans, Patreon) au titre des BNC.",
        "lien": "https://www.conseil-etat.fr/fr/arianeweb/"
    },
    {
        "source": "CJUE",
        "categorie": "jurisprudence",
        "titre": "Arrêt CJUE : Règles de territorialité de la TVA applicables aux prestations de services numériques transfrontalières.",
        "lien": "https://curia.europa.eu/"
    },
    {
        "source": "BOFiP",
        "categorie": "bofip",
        "titre": "Mise à jour BOFiP : Articulation entre l'abattement forfaitaire de 34% (Micro-BNC) et la déduction des frais réels pour les influenceurs.",
        "lien": "https://bofip.impots.gouv.fr/"
    },
    {
        "source": "Dalloz Actualité",
        "categorie": "doctrine",
        "titre": "Chronique : Requalification fiscale des avantages en nature et cadeaux reçus par les créateurs de contenu (Art. 79 du CGI).",
        "lien": "https://www.dalloz-actualite.fr/"
    },
    {
        "source": "Navis Fiscal",
        "categorie": "doctrine",
        "titre": "Arbitrage de structure : IS vs IR (SASU ou Entreprise Individuelle) pour l'activité de streaming à forte croissance.",
        "lien": "https://www.efl.fr/"
    }
]

try:
    # 2. Lecture du fichier de structure HTML
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # On prépare nos chaînes de caractères pour stocker les liens de veille
    liens_jurisprudence = ""
    liens_bofip = ""
    liens_doctrine = ""

    # 3. Tri et mise en forme automatique des alertes sous forme de liens cliquables
    for alerte in flux_actualites:
        bloc_html = f"""
        <div class="veille-item" style="background: white; padding: 1rem; margin-bottom: 0.8rem; border-radius: 6px; border-left: 4px solid #c5a059; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <span style="font-size: 0.8rem; font-weight: bold; color: #718096; text-transform: uppercase;">[{alerte['source']}]</span>
            <p style="margin: 0.3rem 0; font-weight: 500; color: #2d3748;">{alerte['titre']}</p>
            <a href="{alerte['lien']}" target="_blank" style="font-size: 0.85rem; color: #c5a059; text-decoration: none; font-weight: bold;">→ Accéder à la source officielle</a>
        </div>
        """
        if alerte["categorie"] == "jurisprudence":
            liens_jurisprudence += bloc_html
        elif alerte["categorie"] == "bofip":
            liens_bofip += bloc_html
        elif alerte["categorie"] == "doctrine":
            liens_doctrine += bloc_html

    # 4. Injection automatique dans les conteneurs du site de ton amie
    html = html.replace('<div id="jurisprudence-container"></div>', f'<div id="jurisprudence-container">\n{liens_jurisprudence}\n</div>')
    html = html.replace('<div id="bofip-container"></div>', f'<div id="bofip-container">\n{liens_bofip}\n</div>')
    html = html.replace('<div id="doctrine-container"></div>', f'<div id="doctrine-container">\n{liens_doctrine}\n</div>')

    # 5. Sauvegarde du fichier mis à jour
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Le flux de veille automatique a été rafraîchi avec succès !")

except Exception as e:
    print(f"Erreur lors de la mise à jour de la veille : {e}")
    raise e
