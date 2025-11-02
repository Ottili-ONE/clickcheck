# ClickCheck AI - API Dokumentation

## 📚 Inhaltsverzeichnis

1. [Überblick](#überblick)
2. [Authentifizierung](#authentifizierung)
3. [Endpoints](#endpoints)
   - [Scans](#scans)
   - [Blacklist](#blacklist)
   - [API Tokens](#api-tokens)
   - [Organisationen](#organisationen)
   - [Export](#export)
   - [Custom Blacklist](#custom-blacklist)
4. [Rate Limits](#rate-limits)
5. [Pricing](#pricing)
6. [Fehlerbehandlung](#fehlerbehandlung)
7. [Code-Beispiele](#code-beispiele)

---

## Überblick

Die ClickCheck AI API ermöglicht programmatischen Zugriff auf alle Features von ClickCheck AI. Die API verwendet REST-Prinzipien und gibt Antworten im JSON-Format zurück.

**Base URL:** `https://api.getclickcheck.com/api/v1` (Production)  
**Development:** `http://localhost:8000/api/v1`

**Alle Anfragen müssen mit einem API Token authentifiziert werden** (außer öffentliche Endpoints).

---

## Authentifizierung

### API Token erstellen

1. **Erstelle einen API Token** im Dashboard (`/api-tokens`)
2. **Kopiere den Token** - er wird nur einmal angezeigt!
3. **Nutze den Token** in jedem Request im `Authorization` Header:

```
Authorization: Bearer YOUR_API_TOKEN
```

### Token-Format

Der Token ist eine Base64-encodierte Zeichenkette (ca. 64 Zeichen).

**⚠️ WICHTIG:** Tokens sind dauerhaft gültig bis sie gelöscht werden. Bewahre sie sicher auf!

---

## Endpoints

### Scans

#### `POST /scans/analyze`

Analysiert eine URL auf Sicherheits- und Datenschutz-Risiken.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response (200 OK):**
```json
{
  "id": 123,
  "url": "https://example.com",
  "domain": "example.com",
  "status": "SAFE",
  "score": 0.15,
  "summary": "Website ist relativ sicher...",
  "ai_analysis": {
    "tldr": [
      "Datenweitergabe an 2 Drittanbieter",
      "Tracker werden erwähnt",
      "Opt-out verfügbar"
    ],
    "risk_score": 0.15,
    "recommendation": "SAFE",
    "details": {
      "data_sharing_count": 2,
      "trackers_mentioned": true,
      "opt_out_available": true,
      "gdpr_compliant": true,
      "concerns": []
    }
  },
  "virustotal_data": {
    "data": {
      "attributes": {
        "last_analysis_stats": {
          "harmless": 65,
          "malicious": 0,
          "suspicious": 0,
          "undetected": 10
        },
        "reputation": 0
      }
    }
  },
  "virustotal_risk": 0.0,
  "privacy_document_url": "https://example.com/privacy",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Status-Codes:**
- `SAFE` - Niedriges Risiko (🟢)
- `CAUTION` - Mittleres Risiko (🟡)
- `UNSAFE` - Hohes Risiko (🔴)

**Kosten:** 0.012€ pro Scan (wird vom Guthaben abgezogen, reduziert von 0.032€)

---

### Blacklist

#### `GET /blacklist/check`

Prüft, ob eine Domain oder URL auf der ClickCheck Blacklist steht.

**Query Parameters:**
- `domain` (required) - Domain-Name (z.B. "example.com")
- `url` (optional) - Vollständige URL

**Response (200 OK):**
```json
{
  "is_blacklisted": true,
  "entry": {
    "id": 42,
    "domain": "example.com",
    "url": null,
    "reason": "Phishing-Versuche erkannt",
    "severity": "high",
    "source": "community",
    "created_at": "2025-01-10T08:00:00Z"
  }
}
```

**Response (200 OK) - Nicht blacklisted:**
```json
{
  "is_blacklisted": false,
  "entry": null
}
```

#### `POST /blacklist/report`

Meldet eine Domain zur Aufnahme in die Blacklist.

**🆕 REWARD SYSTEM:** Wenn der Report akzeptiert wird (verifiziert und zur Blacklist hinzugefügt), erhältst du **0.001€ (1 Credit)** als Belohnung auf dein API-Guthaben!

**Request Body:**
```json
{
  "domain": "example.com",
  "url": "https://example.com/page" (optional),
  "reason": "Warum ist diese Domain unsicher?" (optional),
  "evidence": "Weitere Details..." (optional)
}
```

**Response (200 OK):**
```json
{
  "id": 789,
  "domain": "example.com",
  "status": "verified",
  "reward_credits": 0.001,
  "message": "Domain example.com has been added to the blacklist. You received 0.001€ as reward.",
  "created_at": "2025-01-15T10:00:00Z"
}
```

**Status-Werte:**
- `pending` - Wird geprüft
- `verified` - Auf Blacklist hinzugefügt (Belohnung erhalten!)
- `rejected` - Nicht als unsicher eingestuft

**Hinweis:** Reports werden automatisch mit AI, VirusTotal und Online-Recherche geprüft.

#### `GET /blacklist/my-reports`

Listet alle eigenen Reports auf.

**Response (200 OK):**
```json
[
  {
    "id": 789,
    "domain": "example.com",
    "reason": "Phishing",
    "status": "approved",
    "created_at": "2025-01-15T10:00:00Z"
  }
]
```

**Status-Werte:**
- `pending` - Wird geprüft
- `approved` - Auf Blacklist hinzugefügt
- `rejected` - Nicht als unsicher eingestuft

---

### API Tokens

#### `POST /api-tokens`

Erstellt einen neuen API Token.

**Request Body:**
```json
{
  "name": "Production API" (optional)
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Production API",
  "token": "ccai_abc123def456...", // ⚠️ NUR EINMAL SICHTBAR!
  "balance_credits": 0.0,
  "total_used_credits": 0.0,
  "is_active": true,
  "created_at": "2025-01-15T10:00:00Z"
}
```

#### `GET /api-tokens`

Listet alle API Tokens des Nutzers auf.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Production API",
    "balance_credits": 10.50,
    "total_used_credits": 5.20,
    "is_active": true,
    "last_used": "2025-01-15T09:30:00Z",
    "created_at": "2025-01-10T08:00:00Z"
  }
]
```

#### `DELETE /api-tokens/{token_id}`

Löscht einen API Token. Der Token wird sofort deaktiviert.

**Response:** 204 No Content

#### `POST /api-tokens/deposit`

Erstellt eine Stripe Checkout Session für Guthaben-Aufladung.

**Request Body:**
```json
{
  "amount": 10.00,
  "api_token_id": 1 (optional - wenn nicht angegeben, wird der erste Token verwendet)
}
```

**Response (200 OK):**
```json
{
  "checkout_url": "https://checkout.stripe.com/..."
}
```

**Kosten:** 1:1 (10€ = 10€ Guthaben)

---

### Organisationen

#### `POST /organizations`

Erstellt eine neue Organisation (Business-only).

**Request Body:**
```json
{
  "name": "Meine Firma GmbH"
}
```

**Response (200 OK):**
```json
{
  "id": 5,
  "name": "Meine Firma GmbH",
  "owner_id": 123,
  "max_members": -1,
  "custom_blacklist_enabled": true,
  "created_at": "2025-01-15T10:00:00Z"
}
```

#### `GET /organizations`

Gibt die Organisation des aktuellen Nutzers zurück.

**Response (200 OK):**
```json
{
  "id": 5,
  "name": "Meine Firma GmbH",
  "owner_id": 123,
  "max_members": -1,
  "custom_blacklist_enabled": true,
  "created_at": "2025-01-15T10:00:00Z"
}
```

#### `POST /organizations/{org_id}/members`

Lädt ein Mitglied zur Organisation ein.

**Request Body:**
```json
{
  "email": "mitarbeiter@example.com",
  "role": "member" (optional, default: "member")
}
```

**Response (200 OK):**
```json
{
  "id": 42,
  "user_id": 456,
  "organization_id": 5,
  "role": "member",
  "is_paid": false,
  "discount_percentage": 0,
  "joined_at": "2025-01-15T10:00:00Z"
}
```

#### `GET /organizations/{org_id}/members`

Listet alle Mitglieder einer Organisation auf.

**Response (200 OK):**
```json
[
  {
    "id": 42,
    "user_id": 456,
    "user_email": "mitarbeiter@example.com",
    "user_name": "Max Mustermann",
    "role": "member",
    "is_paid": true,
    "joined_at": "2025-01-15T10:00:00Z"
  }
]
```

#### `DELETE /organizations/{org_id}/members/{member_id}`

Entfernt ein Mitglied aus der Organisation.

**Response:** 204 No Content

---

### Export

#### `GET /exports/pdf`

Exportiert Scans als PDF (Pro/Business-only).

**Query Parameters:**
- `scan_ids` (optional) - Komma-getrennte Scan-IDs (z.B. "1,2,3")
- `start_date` (optional) - Start-Datum (YYYY-MM-DD)
- `end_date` (optional) - End-Datum (YYYY-MM-DD)

**Response:** PDF-Datei (Content-Type: `application/pdf`)

#### `GET /exports/csv`

Exportiert Scans als CSV (Pro/Business-only).

**Query Parameters:** Gleiche wie PDF

**Response:** CSV-Datei (Content-Type: `text/csv`)

#### `GET /exports/xlsx`

Exportiert Scans als Excel (Business-only).

**Query Parameters:** Gleiche wie PDF

**Response:** Excel-Datei (Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`)

---

### Custom Blacklist

#### `POST /custom-blacklist/upload`

Lädt eine Custom Blacklist hoch (Business-only).

**Request (multipart/form-data):**
- `name` - Name der Blacklist (z.B. "Unser Partner-Blacklist")
- `file` - CSV oder Text-Datei (eine Domain pro Zeile)

**CSV-Format:**
```csv
domain,reason
example1.com,Phishing
example2.com,Malware
```

**Text-Format:**
```
example1.com
example2.com
example3.com
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Blacklist 'Unser Partner-Blacklist' uploaded successfully",
  "domains_added": 42,
  "domains_skipped": 3,
  "blacklist_id": 7
}
```

#### `GET /custom-blacklist`

Listet alle Custom Blacklists auf.

**Response (200 OK):**
```json
[
  {
    "id": 7,
    "organization_id": 5,
    "name": "Unser Partner-Blacklist",
    "domain_count": 42,
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
  }
]
```

#### `GET /custom-blacklist/{blacklist_id}/domains`

Gibt alle Domains einer Custom Blacklist zurück.

**Response (200 OK):**
```json
{
  "id": 7,
  "name": "Unser Partner-Blacklist",
  "domains": [
    "example1.com",
    "example2.com",
    "example3.com"
  ],
  "domain_count": 3
}
```

#### `DELETE /custom-blacklist/{blacklist_id}`

Löscht eine Custom Blacklist.

**Response:** 204 No Content

---

## Rate Limits

**Free Plan:**
- 3 Scans pro Tag

**Pro Plan:**
- Unbegrenzte Scans
- Rate Limit: 100 Scans/Minute

**Business Plan:**
- Unbegrenzte Scans
- Rate Limit: 500 Scans/Minute

**API Token (Credits-basiert):**
- Kein tägliches Limit
- Nur durch Guthaben begrenzt
- **Plan-basierte Rate Limits:**
  - **FREE**: 10 Requests/Minute
  - **PRO**: 60 Requests/Minute
  - **BUSINESS**: 300 Requests/Minute (höchstes Limit)

Bei Überschreitung:
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## Pricing

### API-Nutzung (Credits)

**🆕 Kosten pro Scan: 0.012€ (reduziert von 0.032€)**

**Breakdown:**
- OpenAI API (GPT-4o-mini): ~0.002€ pro Scan
- Server-Kosten (optimiert): ~0.01€ pro Scan
- **Gesamt: 0.012€**

**Beispiel:**
- 10€ Guthaben = ~833 Scans (vorher: 312)
- 100€ Guthaben = ~8.333 Scans (vorher: 3.125)

**🆕 Belohnungen:**
- **Blacklist Reports:** 0.001€ (1 Credit) für jeden akzeptierten Domain-Report

**Mindestbetrag:** 1€ (kann jederzeit aufgeladen werden)

### Subscription Plans

| Plan | Preis/Monat | Scans/Tag | Features |
|------|------------|-----------|----------|
| **FREE** | Kostenlos | 3 | Basis-Scans, Historie |
| **PRO** | 3,49€ | Unbegrenzt | + VirusTotal, Blacklist, PDF/CSV Export |
| **BUSINESS** | 9,99€ | Unbegrenzt | + API, Excel Export, Custom Blacklist, Teams |

---

## Fehlerbehandlung

### HTTP Status Codes

- `200 OK` - Erfolgreich
- `201 Created` - Ressource erstellt
- `204 No Content` - Erfolgreich, keine Antwort-Daten
- `400 Bad Request` - Ungültige Anfrage
- `401 Unauthorized` - Token fehlt oder ungültig
- `403 Forbidden` - Keine Berechtigung
- `404 Not Found` - Ressource nicht gefunden
- `429 Too Many Requests` - Rate Limit überschritten
- `500 Internal Server Error` - Server-Fehler

### Fehler-Response Format

```json
{
  "detail": "Fehlerbeschreibung"
}
```

**Beispiele:**

**401 Unauthorized:**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden:**
```json
{
  "detail": "This feature is only available for PRO/BUSINESS subscribers"
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

**400 Bad Request:**
```json
{
  "detail": "Invalid URL format"
}
```

---

## Python SDK (PyPi)

**Installation:**
```bash
pip install clickcheck
```

**Quick Start:**
```python
from clickcheck import ClickCheckClient

client = ClickCheckClient(api_token="your_api_token")

# Scan URL
result = client.scan_url("https://example.com")
print(f"Status: {result['status']}, Score: {result['score']}")

# Check blacklist
check = client.check_blacklist("suspicious.com")
if check['blacklisted']:
    print(f"⚠️ {check['domain']} is blacklisted!")

# Report domain (earn 0.001€ reward if accepted!)
report = client.report_blacklist(
    domain="malicious.com",
    reason="Phishing"
)
if report['reward_credits']:
    print(f"✅ Earned {report['reward_credits']:.3f}€!")

# Check balance
balance = client.get_balance()
print(f"Balance: {balance['balance_credits']:.4f}€")
```

**GitHub:** [https://github.com/clickcheck/clickcheck-python](https://github.com/clickcheck/clickcheck-python)

**Vollständige Dokumentation:** Siehe README.md im Repository

---

## Code-Beispiele

### Python

```python
import requests

API_BASE_URL = "http://localhost:8000/api/v1"
API_TOKEN = "YOUR_API_TOKEN"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Scan durchführen
response = requests.post(
    f"{API_BASE_URL}/scans/analyze",
    headers=headers,
    json={"url": "https://example.com"}
)

scan_result = response.json()
print(f"Status: {scan_result['status']}")
print(f"Score: {scan_result['score']}")

# Blacklist-Check
response = requests.get(
    f"{API_BASE_URL}/blacklist/check",
    headers=headers,
    params={"domain": "example.com"}
)

blacklist_result = response.json()
if blacklist_result["is_blacklisted"]:
    print(f"⚠️ Domain ist auf der Blacklist: {blacklist_result['entry']['reason']}")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const API_BASE_URL = 'http://localhost:8000/api/v1';
const API_TOKEN = 'YOUR_API_TOKEN';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json'
  }
});

// Scan durchführen
async function scanUrl(url) {
  try {
    const response = await api.post('/scans/analyze', { url });
    console.log('Status:', response.data.status);
    console.log('Score:', response.data.score);
    return response.data;
  } catch (error) {
    console.error('Fehler:', error.response?.data?.detail || error.message);
  }
}

// Blacklist-Check
async function checkBlacklist(domain) {
  try {
    const response = await api.get('/blacklist/check', {
      params: { domain }
    });
    
    if (response.data.is_blacklisted) {
      console.log('⚠️ Domain ist auf der Blacklist:', response.data.entry.reason);
    } else {
      console.log('✅ Domain ist nicht auf der Blacklist');
    }
    
    return response.data;
  } catch (error) {
    console.error('Fehler:', error.response?.data?.detail || error.message);
  }
}

// Beispiel-Nutzung
scanUrl('https://example.com');
checkBlacklist('example.com');
```

### cURL

```bash
# Scan durchführen
curl -X POST "http://localhost:8000/api/v1/scans/analyze" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Blacklist-Check
curl -X GET "http://localhost:8000/api/v1/blacklist/check?domain=example.com" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# API Token erstellen (benötigt User-Auth, nicht API Token)
curl -X POST "http://localhost:8000/api/v1/api-tokens" \
  -H "Authorization: Bearer USER_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My API Token"}'

# Guthaben-Aufladung starten
curl -X POST "http://localhost:8000/api/v1/api-tokens/deposit" \
  -H "Authorization: Bearer USER_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10.00, "api_token_id": 1}'
```

### PHP

```php
<?php

$apiBaseUrl = 'http://localhost:8000/api/v1';
$apiToken = 'YOUR_API_TOKEN';

// Scan durchführen
function scanUrl($url, $apiBaseUrl, $apiToken) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiBaseUrl . '/scans/analyze');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $apiToken,
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['url' => $url]));
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        return json_decode($response, true);
    } else {
        throw new Exception('API Error: ' . $response);
    }
}

// Beispiel
try {
    $result = scanUrl('https://example.com', $apiBaseUrl, $apiToken);
    echo "Status: " . $result['status'] . "\n";
    echo "Score: " . $result['score'] . "\n";
} catch (Exception $e) {
    echo "Fehler: " . $e->getMessage() . "\n";
}
?>
```

---

## Webhooks

**⚠️ NOCH NICHT IMPLEMENTIERT** - Geplant für v2.0

Geplante Events:
- `scan.completed` - Scan abgeschlossen
- `blacklist.updated` - Blacklist-Eintrag hinzugefügt/entfernt
- `credits.low` - Guthaben unter 1€

---

## Support

**API-Support:**
- E-Mail: api@clickcheck.ai
- Dokumentation: https://docs.clickcheck.ai
- GitHub Issues: https://github.com/clickcheck-ai/api-issues

**Business-Kunden:**
- Dedicated Support per E-Mail
- Priority Bug-Fixes
- Feature Requests

---

## Changelog

### v1.0.0 (2025-01-15)
- Initial API Release
- Scan-Endpoints
- Blacklist-API
- API Token Management
- Organisation-Management
- Export-Features
- Custom Blacklist

---

**© 2025 ClickCheck AI. Alle Rechte vorbehalten.**

