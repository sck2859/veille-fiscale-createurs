import os

# 1. Base de données de la veille fiscale
flux_actualites = [
    {
        "source": "Conseil d'État",
        "categorie": "jurisprudence",
        "influenceur": True,
        "titre": "Arrêt CE, 15 mars 2026 : Imposition des gains issus de plateformes étrangères (OnlyFans, Patreon) au titre des BNC professionnels.",
        "lien": "https://www.conseil-etat.fr/fr/arianeweb/"
    },
    {
        "source": "CJUE",
        "categorie": "jurisprudence",
        "influenceur": False,
        "titre": "Arrêt CJUE : Règles de territorialité de la TVA applicables aux prestations de services numériques transfrontalières.",
        "lien": "https://curia.europa.eu/"
    },
    {
        "source": "BOFiP",
        "categorie": "bofip",
        "influenceur": True,
        "titre": "Mise à jour BOFiP : Articulation entre l'abattement forfaitaire de 34% (Micro-BNC) et la déduction des frais réels pour les influenceurs et créateurs de contenu.",
        "lien": "https://bofip.impots.gouv.fr/"
    },
    {
        "source": "Dalloz Actualité",
        "categorie": "doctrine",
        "influenceur": True,
        "titre": "Chronique : Requalification fiscale des avantages en nature et cadeaux reçus par les créateurs de contenu (Art. 79 du CGI).",
        "lien": "https://www.dalloz-actualite.fr/"
    },
    {
        "source": "Navis Fiscal",
        "categorie": "doctrine",
        "influenceur": True,
        "titre": "Arbitrage de structure : IS vs IR (SASU ou Entreprise Individuelle) pour l'activité de streaming à forte croissance.",
        "lien": "https://www.efl.fr/"
    }
]

try:
    # 2. Lecture du fichier de structure HTML
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Initialisation des chaînes pour chaque conteneur
    liens_memoire = ""
    liens_jurisprudence = ""
    liens_bofip = ""
    liens_doctrine = ""

    # 3. Tri et formatage des alertes
    for alerte in flux_actualites:
        bloc_html = f"""
        <div class="veille-item" style="background: white; padding: 1rem; margin-bottom: 0.8rem; border-radius: 6px; border-left: 4px solid #c5a059; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <span style="font-size: 0.8rem; font-weight: bold; color: #718096; text-transform: uppercase;">[{alerte['source']}]</span>
            <p style="margin: 0.3rem 0; font-weight: 500; color: #2d3748;">{alerte['titre']}</p>
            <a href="{alerte['lien']}" target="_blank" style="font-size: 0.85rem; color: #c5a059; text-decoration: none; font-weight: bold;">→ Accéder à la source officielle</a>
        </div>
        """
        
        # Si ça concerne directement les influenceurs, on le pousse aussi dans le focus mémoire
        if alerte["influenceur"]:
            liens_memoire += bloc_html

        # Classement classique par type de document
        if alerte["categorie"] == "jurisprudence":
            liens_jurisprudence += bloc_html
        elif alerte["categorie"] == "bofip":
            liens_bofip += bloc_html
        elif alerte["categorie"] == "doctrine":
            liens_doctrine += bloc_html

    # 4. Injection par remplacement d'identifiants (sans doublons)
    html = html.replace('<div id="memoire-container"></div>', f'<div id="memoire-container">\n{liens_memoire}\n</div>')
    html = html.replace('<div id="jurisprudence-container"></div>', f'<div id="jurisprudence-container">\n{liens_jurisprudence}\n</div>')
    html = html.replace('<div id="bofip-container"></div>', f'<div id="bofip-container">\n{liens_bofip}\n</div>')
    html = html.replace('<div id="doctrine-container"></div>', f'<div id="doctrine-container">\n{liens_doctrine}\n</div>')

    # 5. Sauvegarde
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Le flux de veille et l'onglet mémoire ont été mis à jour avec succès !")

except Exception as e:
    print(f"Erreur d'exécution : {e}")
    raise e
