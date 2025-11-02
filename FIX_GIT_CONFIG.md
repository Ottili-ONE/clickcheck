# Git User Config schnell setzen

Falls das Script wegen fehlender Git Config abbricht, setze sie so:

```powershell
cd "F:\neu\ClickCheck AI\clickcheck-api"

# Git Config setzen (einmalig)
git config --global user.name "ClickCheck AI"
git config --global user.email "support@getclickcheck.com"

# Danach Script erneut ausführen
.\setup-github.ps1
```

Oder mit deinen eigenen Daten:
```powershell
git config --global user.name "Dein Name"
git config --global user.email "deine@email.com"
```

Die Config wird global gesetzt und für alle Git Repositories verwendet.

