# Quick Start Guide - ClickCheck Python SDK

## 🚀 GitHub Repository Setup

### Option 1: Automatisches Script (Empfohlen)

```powershell
cd "F:\neu\ClickCheck AI\clickcheck-api"
.\setup-github.ps1
```

Das Script prüft automatisch, ob Git verfügbar ist und richtet alles ein.

### Option 2: Manuelle Git Befehle

Wenn Git installiert ist:

```bash
cd "F:\neu\ClickCheck AI\clickcheck-api"
git init
git remote add origin git@github.com:Ottili-ONE/clickcheck.git
git branch -M main
git add .
git commit -m "Initial commit: ClickCheck Python SDK v1.0.0"
git push -u origin main
```

### Option 3: GitHub Web Interface

1. Gehe zu: https://github.com/Ottili-ONE/clickcheck
2. Klicke "Add file" → "Upload files"
3. Ziehe alle Dateien aus dem `clickcheck-api` Ordner
4. Commit message: "Initial commit: ClickCheck Python SDK v1.0.0"
5. Klicke "Commit changes"

## 📦 PyPI Veröffentlichung

### 1. PyPI Account & Token

1. Erstelle Account: https://pypi.org/account/register/
2. Erstelle Token: https://pypi.org/manage/account/token/
3. Kopiere Token (beginnt mit `pypi-...`)

### 2. GitHub Secret hinzufügen

1. Gehe zu: https://github.com/Ottili-ONE/clickcheck/settings/secrets/actions
2. "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Dein PyPI Token
5. "Add secret"

### 3. Package testen (lokal)

```bash
cd "F:\neu\ClickCheck AI\clickcheck-api"
pip install build twine
python -m build
```

### 4. Release erstellen (automatisches Publishing)

1. Gehe zu: https://github.com/Ottili-ONE/clickcheck/releases/new
2. **Tag:** `v1.0.0`
3. **Title:** `v1.0.0 - Initial Release`
4. **Description:** Siehe CHANGELOG.md
5. "Publish release"

GitHub Actions veröffentlicht automatisch auf PyPI! ✅

### 5. Installation testen

Nach dem Publishing:

```bash
pip install clickcheck
python -c "from clickcheck import ClickCheckClient; print('✅ Erfolgreich!')"
```

## 📚 Nächste Schritte

- Repository Description setzen (siehe GITHUB_SETUP.md)
- Topics hinzufügen (siehe GITHUB_SETUP.md)
- Package testen: `pip install clickcheck`
- Dokumentation erweitern falls nötig

