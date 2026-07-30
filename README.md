# Cinevora AI

**From Story to Screen — Powered by AI**

Cinevora AI is a Streamlit filmmaking workspace that combines screenplay writing, structured AI analysis, revision tools, storyboard concept art, production planning, budgeting, pitching, collaboration, talent, consultation, university workflows, and a film-community workspace.

## AI services

- Gemini: screenplay PDF analysis and generative writing/development tools.
- Cloudflare Workers AI / FLUX.1 Schnell: storyboard and poster concept art.

## Feature set

Cinevora includes all of these feature categories in the current build:

- Screenplay Writing
- Professional Script Formatting
- Import / Export Script Files, including TXT, Fountain, DOCX, PDF, and basic FDX interchange
- AI Script Analysis
- Story Structure Analysis
- Character Analysis
- Dialogue Analysis
- Theme Analysis
- Scene Analysis
- AI Improvement Suggestions
- AI Story Consultant
- AI Story Generation
- AI Script Rewrite Assistant
- AI Audience Prediction
- Similar Movie Comparison
- AI Voice Consultant
- Emotional Timeline
- Storyboard Generator
- Production Planning
- Budget Estimation
- Pitch Deck Generator
- Casting Support
- Collaboration Tools
- Talent Marketplace workspace
- Professional Consultation workspace
- University Platform workspace
- Film Community workspace

The industry/community modules are functional workspace implementations. A public production service should add authentication, roles/permissions, moderation, secure messaging, verified talent/consultants, and persistent hosted storage.

## Local setup

1. Install Python 3.11 or 3.12.
2. Open this folder in VS Code.
3. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Copy `.env.example` to `.env` and add:

```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-3.6-flash
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_workers_ai_token
```

6. Run:

```powershell
python -m streamlit run app.py
```

## Streamlit Community Cloud

Upload the contents of this `Cinevora_AI` folder to the root of a GitHub repository. Do not upload `.env`, `.venv`, `data/`, or `.streamlit/secrets.toml`.

Use `app.py` as the Streamlit main file. In Streamlit Secrets add:

```toml
GEMINI_API_KEY = "your_key"
GEMINI_MODEL = "gemini-3.6-flash"
CLOUDFLARE_ACCOUNT_ID = "your_account_id"
CLOUDFLARE_API_TOKEN = "your_workers_ai_token"
```

The cinematic intro includes a locally packaged sound cue. It begins after the user presses **Enter Cinevora AI**, which also avoids common browser restrictions on unsolicited audio autoplay.

## Storage note

Saved analyses and the collaboration/community/marketplace/university/consultation workspace currently use local SQLite (`data/cinevora.db`). Local disk on Streamlit Community Cloud is not suitable for permanent multi-user records. For production, replace it with a hosted database such as PostgreSQL/Supabase and add authentication.

## Tests

```powershell
pytest -q
```
