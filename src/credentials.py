"""Some functions to get credentials."""

import os
from pathlib import Path
from typing import Optional

from src.utilities import read_json_file
from src.utilities import dprint
from src.utilities import ciao
_ = dprint, ciao


creds_dir = Path.home() / ".credentials" / "hermione"


def get_key(name: str) -> str:
    """Get the Cohere API key."""
    key_json = read_json_file(creds_dir / 'credentials.json')
    api_key = key_json[name]
    return api_key


def get_cred_file(filename: str):
    """Return the credentials file."""
    cred_file = creds_dir / filename
    return cred_file


def set_env_key(name: str, env_name: Optional[str] = None):
    """Set an evnironment variable from the credentials."""
    if not env_name:
        env_name = name
    value = get_key(name)
    os.environ[env_name] = value
