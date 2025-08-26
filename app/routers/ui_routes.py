from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from app.core.security import require_ui_auth, ui_auth_state, issue_cookie

router = APIRouter()

HTML_PAGE = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Printer API - Web Interface</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        input, textarea, button { margin: 5px 0; padding: 10px; width: 100%; box-sizing: border-box; }
        button { background: #007cba; color: white; border: none; cursor: pointer; }
        button:hover { background: #005a8a; }
        .login-form { max-width: 300px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖨️ Printer API</h1>
        <p>Web-Interface für den Belegdrucker</p>
        
        <!-- Login Form -->
        <div class="login-form">
            <h2>Login erforderlich</h2>
            <form method="post">
                <input type="password" name="password" placeholder="Passwort" required>
                <label>
                    <input type="checkbox" name="remember"> Angemeldet bleiben
                </label>
                <button type="submit">Anmelden</button>
            </form>
        </div>
        
        <!-- Print Form -->
        <div id="print-interface" style="display: none;">
            <h2>Text drucken</h2>
            <form method="post" action="/ui/print">
                <input type="text" name="title" placeholder="Titel" value="AUFGABE">
                <textarea name="text" rows="5" placeholder="Text zum Drucken"></textarea>
                <label>
                    <input type="checkbox" name="add_datetime" checked> Datum/Zeit hinzufügen
                </label>
                <label>
                    <input type="checkbox" name="cut" checked> Papier abschneiden
                </label>
                <button type="submit">Drucken</button>
            </form>
        </div>
    </div>
    <script>
        const authed = document.cookie.includes('ui_token');
        if (!authed) {
            document.querySelector('.login-form').style.display = 'block';
            document.getElementById('print-interface').style.display = 'none';
        } else {
            document.querySelector('.login-form').style.display = 'none';
            document.getElementById('print-interface').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@router.get("/ui", response_class=HTMLResponse)
async def web_ui_get(request: Request):
    if require_ui_auth(request):
        return HTMLResponse(HTML_PAGE.replace('style="display: none;"', ''))
    else:
        return HTMLResponse(HTML_PAGE)

@router.post("/ui")
async def web_ui_post(request: Request, password: Optional[str] = Form(None), remember: bool = Form(False)):
    authed, should_set_cookie = ui_auth_state(request, password, remember)
    if authed:
        resp = RedirectResponse("/ui", status_code=303)
        if should_set_cookie:
            issue_cookie(resp)
        return resp
    else:
        return HTMLResponse(HTML_PAGE)

@router.post("/ui/print")
async def ui_print(request: Request, title: str = Form(""), text: str = Form(""), add_datetime: bool = Form(False), cut: bool = Form(True)):
    if not require_ui_auth(request):
        return RedirectResponse("/ui", status_code=302)
    # Drucklogik nach Bedarf einfügen
    return RedirectResponse("/ui?printed=1", status_code=302)
