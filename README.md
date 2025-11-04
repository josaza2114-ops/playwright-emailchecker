# Playwright Email Checker (Python)

Small Playwright script to check a Gmail inbox.  
It signs in once (manually or by scripted steps), saves the **storage state** (`storage_state.json`), and then reuses that session to read the inbox.

> ⚠️ Google can expire sessions at any time. For long-term automation use the **Gmail API**. This repo is for basic checks and local testing.

---

## Requirements

- **Python 3.10+**
- **Playwright** and browser binaries
- **python-dotenv** (to load `.env` secrets)

---

## Project structure

```
.
├─ app.py          # Uses saved storage state to open Gmail and read rows
├─ get_creds.py    # Logs in and saves storage_state.json
├─ .env            # Your secrets
├─ storage_state.json  # Saved cookies/tokens (generated)
└─ README.md
```

---

## Setup

### 1) Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install --upgrade pip
```

### 2) Install dependencies

```powershell
pip install playwright python-dotenv
playwright install
```

### 3) Add your environment variables

Create a file named **`.env`** in the project root:

```
EMAIL_ADDRESS=your.name@gmail.com
EMAIL_PASSWORD=your_password_or_app_password
GMAIL_URL=https://accounts.google.com/signin/v2/identifier?service=mail
```

> Tip: If your account uses 2-Step Verification, prefer an **App Password**.

### 4) Save your login session (storage state)

Run the helper:

```powershell
python get_creds.py
```

What it does:

- Launches Chromium **headful**.
- Navigates to `GMAIL_URL`.
- Fills email and password from `.env`.
- Saves cookies and tokens to **`storage_state.json`**.

If Google asks for extra verification, complete it in the opened window.  
When the window closes, `storage_state.json` should exist.

---

## Run the checker

```powershell
python app.py
```

What it does:

- Loads **`storage_state.json`** so you are already signed in.
- Opens Gmail and queries the inbox table rows.
- Prints any “new” emails it finds (based on row selectors used in `app.py`).

Output example:

```
New email from Example Sender: Welcome!
------------------------------
Total new emails: 1
```

---

## Notes on selectors (in `app.py`)

- It targets rows with `div.UI table tr`.
- It extracts:
  - **Sender**: `td span[email]:visible`
  - **Title/Subject**: `td span[data-thread-id]:visible`
- Adjust selectors as Gmail UI changes.  
  Use `page.pause()` to inspect the DOM with Playwright Inspector and refine locators.

---

## Troubleshooting

- **“Couldn’t sign you in — This browser or app may not be secure”**  
  Use `get_creds.py` to complete a normal, interactive login. Avoid headless login.  
  If blocked, try again later or sign in manually at `https://mail.google.com/` in the same flow.

- **2FA or device prompts**  
  Approve on your phone or use an **App Password**.

- **Session expired**  
  Delete `storage_state.json` and run `get_creds.py` again.

- **Stuck on loading**  
  Add waits or `page.pause()` in `get_creds.py` to confirm fields are visible before filling.

---

## Security

- Never commit `.env` or session files.

## License

MIT
