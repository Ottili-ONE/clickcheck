# GitHub Repository Setup - Manuelle Anleitung

Da Git möglicherweise nicht im PATH verfügbar ist, hier die manuelle Anleitung:

## 1. Repository initialisieren

Führe diese Befehle im `clickcheck-api` Verzeichnis aus:

```bash
cd "F:\neu\ClickCheck AI\clickcheck-api"
git init
git remote add origin git@github.com:Ottili-ONE/clickcheck.git
git branch -M main
```

## 2. Dateien hinzufügen und committen

```bash
git add .
git commit -m "Initial commit: ClickCheck Python SDK v1.0.0"
```

## 3. Zu GitHub pushen

```bash
git push -u origin main
```

## 4. GitHub Repository Settings

Nach dem ersten Push, gehe zu: https://github.com/Ottili-ONE/clickcheck/settings

**Description setzen:**
```
Official Python SDK for ClickCheck AI API - Analyze website privacy and security risks programmatically. Easy-to-use Python library for scanning websites, checking blacklists, and reporting malicious domains. pip install clickcheck
```

**Topics hinzufügen:**
- `python`
- `api`
- `sdk`
- `security`
- `privacy`
- `website-scanner`
- `clickcheck`

**Website URL:** `https://getclickcheck.com`

## 5. PyPI Setup (nächster Schritt)

Für PyPI Veröffentlichung:
1. Erstelle Account auf https://pypi.org
2. Erstelle API Token
3. Füge als GitHub Secret hinzu: `PYPI_API_TOKEN`
4. Erstelle Release auf GitHub → automatisches Publishing via GitHub Actions

