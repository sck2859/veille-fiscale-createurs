import feedparser
import os
from datetime import datetime

# ============================================
# LIENS FIXES - Sources officielles clés
# Ces liens ne changent pas, ils pointent vers
# les ressources essentielles pour le mémoire
# ============================================

LIENS_FIXES = [
    {
        "source": "BOFiP",
        "categorie": "bofip",
        "influenceur": True,
        "titre": "BOFiP - BNC : Régime des bénéfices non commerciaux (base doctrine administrative)",
        "lien": "https://bofip.impots.gouv.fr/bofip/5626-PGP.html"
    },
    {
        "source": "BOFiP",
        "categorie": "bofip",
        "influenceur": True,
        "titre": "BOFiP - Micro-BNC : Régime micro-fiscal et abattement forfaitaire 34%",
        "lien": "https://bofip.impots.gouv.fr/bofip/1018-PGP.html"
    },
    {
        "source": "BOFiP",
        "categorie": "bofip",
        "influenceur": True,
        "titre": "BOFiP - TVA : Prestations de services numériques et territorialité",
        "lien": "https://bofip.impots.gouv.fr/bofip/2035-PGP.html"
    },
    {
        "source": "BOFiP",
        "categorie": "bofip",
        "influenceur": True,
        "titre": "BOFiP - Droits d'auteur : Régime fiscal des revenus d'auteur (article 93 CGI)",
        "lien": "https://bofip.impots.gouv.fr/bofip/5633-PGP.html"
    },
    {
        "source": "Légifrance",
        "categorie": "bofip",
        "influenceur": True,
        "titre": "CGI Article 92 - Définition des BNC et revenus assimilés",
        "lien": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006302347"
    },
    {
        "source": "Légifrance",
        "categorie": "bofip",
        "influenceur": True,
        "titre": "CGI Article 93 - Détermination du bénéfice imposable en BNC",
        "lien": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036428069"
    },
    {
        "source": "Conseil d'État",
        "categorie": "jurisprudence",
        "influenceur": True,
        "titre": "Recherche Arianeweb - Jurisprudence fiscale BNC et revenus numériques",
        "lien": "https://www.conseil-etat.fr/fr/arianeweb/"
    },
    {
        "source": "CJUE",
        "categorie": "jurisprudence",
        "influenceur": False,
        "titre": "CJUE - Jurisprudence TVA sur services numériques transfrontaliers",
        "lien": "https://curia.europa.eu/juris/recherche.jsf"
    },
]

# ============================================
# FLUX RSS - Sources automatiques
# Ces articles se mettent à jour automatiquement
# ============================================

FEEDS = {
    "jurisprudence": [
        "https://www.conseil-etat.fr/actualites/rss",
        "https://www.actu-juridique.fr/feed/",
    ],
    "bofip": [
        "https://bofip.impots.gouv.fr/flux-rss",
        "https://www.vie-publique.fr/rss.xml",
    ],
    "doctrine": [
        "https://www.village-justice.com/articles/rss.php?domaine=5",
        "https://www.fiscalonline.com/feed",
        "https://www.legalis.net/feed",
    ]
}

# Mots-clés pour filtrer les articles pertinents pour le mémoire
MOTS_CLES_INFLUENCEUR = [
    "influenceur", "créateur", "contenu", "streaming", "youtube",
    "instagram", "tiktok", "twitch", "bnc", "micro-bnc", "numérique",
    "plateforme", "redevance", "droits d'auteur", "onlyfans", "patreon",
    "fiscalité", "impôt", "tva", "revenu"
]

def est_pertinent(titre, resume=""):
    """Vérifie si un article est pertinent pour le sujet du mémoire"""
    texte = (titre + " " + resume).lower()
    return any(mot in texte for mot in MOTS_CLES_INFLUENCEUR)

def faire_bloc(source, titre, lien, badge_nouveau=False):
    """Génère le HTML d'un bloc article"""
    badge = '<span style="background:#c5a059;color:white;font-size:0.7rem;padding:2px 6px;border-radius:10px;margin-left:8px;">🆕 Nouveau</span>' if badge_nouveau else ""
    return f"""
    <div class="veille-item" style="background: white; padding: 1rem; margin-bottom: 0.8rem; border-radius: 6px; border-left: 4px solid #c5a059; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <span style="font-size: 0.8rem; font-weight: bold; color: #718096; text-transform: uppercase;">[{source}]</span>{badge}
        <p style="margin: 0.3rem 0; font-weight: 500; color: #2d3748;">{titre}</p>
        <a href="{lien}" target="_blank" style="font-size: 0.85rem; color: #c5a059; text-decoration: none; font-weight: bold;">→ Accéder à la source officielle</a>
    </div>
    """

# ============================================
# GÉNÉRATION DU CONTENU
# ============================================

liens_memoire = ""
liens_jurisprudence = ""
liens_bofip = ""
liens_doctrine = ""

# 1. Ajout des liens fixes
for item in LIENS_FIXES:
    bloc = faire_bloc(item["source"], item["titre"], item["lien"])
    if item["influenceur"]:
        liens_memoire += bloc
    if item["categorie"] == "jurisprudence":
        liens_jurisprudence += bloc
    elif item["categorie"] == "bofip":
        liens_bofip += bloc
    elif item["categorie"] == "doctrine":
        liens_doctrine += bloc

# 2. Ajout des articles RSS automatiques
for categorie, urls in FEEDS.items():
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                titre = entry.get("title", "Sans titre")
                lien = entry.get("link", "#")
                resume = entry.get("summary", "")
                source = feed.feed.get("title", url)
                pertinent = est_pertinent(titre, resume)
                bloc = faire_bloc(source, titre, lien, badge_nouveau=True)
                if categorie == "jurisprudence":
                    liens_jurisprudence += bloc
                elif categorie == "bofip":
                    liens_bofip += bloc
                elif categorie == "doctrine":
                    liens_doctrine += bloc
                if pertinent:
                    liens_memoire += bloc
        except Exception as e:
            print(f"Erreur sur {url} : {e}")

# Message si aucun contenu
vide = '<p style="color:#718096;font-style:italic;">Aucune actualité récente.</p>'
if not liens_jurisprudence:
    liens_jurisprudence = vide
if not liens_bofip:
    liens_bofip = vide
if not liens_doctrine:
    liens_doctrine = vide
if not liens_memoire:
    liens_memoire = vide

# ============================================
# LECTURE ET RÉÉCRITURE DE L'INDEX.HTML
# ============================================

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Remplacement des containers — méthode robuste
    import re

    html = re.sub(
        r'<div id="memoire-container">.*?</div>',
        f'<div id="memoire-container">{liens_memoire}</div>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<div id="jurisprudence-container">.*?</div>',
        f'<div id="jurisprudence-container">{liens_jurisprudence}</div>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<div id="bofip-container">.*?</div>',
        f'<div id="bofip-container">{liens_bofip}</div>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<div id="doctrine-container">.*?</div>',
        f'<div id="doctrine-container">{liens_doctrine}</div>',
        html, flags=re.DOTALL
    )

    # Mise à jour de la date si elle existe dans le HTML
    html = re.sub(
        r'Dernière mise à jour :.*?(?=<)',
        f'Dernière mise à jour : {datetime.now().strftime("%d/%m/%Y à %H:%M")}',
        html
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Site mis à jour avec succès !")

except Exception as e:
    print(f"❌ Erreur : {e}")
    raise e
