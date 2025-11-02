# PyPI Veröffentlichung - Schritt-für-Schritt Anleitung

## Voraussetzungen

1. **PyPI Account erstellen:**
   - Gehe zu https://pypi.org/account/register/
   - Erstelle einen Account

2. **API Token erstellen:**
   - Gehe zu https://pypi.org/manage/account/token/
   - Erstelle einen neuen API Token (Scope: "Entire account" oder "All projects")
   - **WICHTIG:** Kopiere den Token sofort - er wird nur einmal angezeigt!
   - Format: `pypi-...`

## Option 1: Manuelle Veröffentlichung

### 1. Package builden

```bash
cd "F:\neu\ClickCheck AI\clickcheck-api"

# Build tools installieren
pip install build twine

# Package builden
python -m build
```

Das erstellt:
- `dist/clickcheck-1.0.0.tar.gz` (Source Distribution)
- `dist/clickcheck-1.0.0-py3-none-any.whl` (Wheel)

### 2. Test auf TestPyPI (empfohlen!)

```bash
# Upload zu TestPyPI
python -m twine upload --repository testpypi dist/*

# Testen der Installation
pip install --index-url https://test.pypi.org/simple/ clickcheck
```

Wenn alles funktioniert, weiter mit Production PyPI.

### 3. Production PyPI Upload

```bash
python -m twine upload dist/*
```

Bei der Abfrage nach Credentials:
- **Username:** `__token__`
- **Password:** Dein PyPI API Token (beginnt mit `pypi-...`)

## Option 2: Automatisches Publishing via GitHub Actions

### 1. GitHub Secret hinzufügen

1. Gehe zu: https://github.com/Ottili-ONE/clickcheck/settings/secrets/actions
2. Klicke auf "New repository secret"
3. **Name:** `PYPI_API_TOKEN`
4. **Value:** Dein PyPI API Token
5. Klicke "Add secret"

### 2. Release erstellen

1. Gehe zu: https://github.com/Ottili-ONE/clickcheck/releases/new
2. **Tag version:** `v1.0.0`
3. **Release title:** `v1.0.0 - Initial Release`
4. **Description:** Siehe CHANGELOG.md
5. Klicke "Publish release"

GitHub Actions startet automatisch und veröffentlicht das Package auf PyPI!

## Nach der Veröffentlichung

### Testen der Installation

```bash
pip install clickcheck
```

```python
from clickcheck import ClickCheckClient
print("✅ Installation erfolgreich!")
```

### PyPI Package Seite

Nach dem Upload findest du das Package hier:
- **PyPI:** https://pypi.org/project/clickcheck/
- **GitHub:** https://github.com/Ottili-ONE/clickcheck

## Updates veröffentlichen

1. Version in `setup.py` erhöhen (z.B. `1.0.0` → `1.0.1`)
2. `CHANGELOG.md` aktualisieren
3. Neue Distribution builden: `python -m build`
4. Upload zu PyPI: `python -m twine upload dist/*`
   ODER: Neues Release auf GitHub erstellen (für automatisches Publishing)

## Troubleshooting

**Fehler: "File already exists"**
- Version in `setup.py` erhöhen

**Fehler: "Invalid credentials"**
- Token prüfen (muss mit `__token__` als Username verwendet werden)
- Token neu erstellen falls nötig

**Fehler: "No files found in dist/"**
- Erst `python -m build` ausführen

