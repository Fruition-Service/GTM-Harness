"""API clients for the sequencer platforms (Smartlead, HeyReach).

Auto-loads config/.env (gitignored) if python-dotenv is installed and the
file exists, so SMARTLEAD_API_KEY / HEYREACH_API_KEY are picked up in local
dev without extra setup. In CI, set these via GitHub Secrets/Doppler
instead — see AGENTS.md §1.3.
"""
from pathlib import Path

try:
    from dotenv import load_dotenv

    _env_path = Path(__file__).resolve().parent.parent.parent / "config" / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass
