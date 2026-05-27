import json
import os
import pathlib

from dotenv import load_dotenv

CONFIG_PATH = pathlib.Path.home() / ".config" / "howlong" / "config.json"


def get_api_key() -> str:
    load_dotenv()

    # Dev path
    if key := os.getenv("YOUTUBE_API_KEY"):
        return key

    # End user path
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())["api_key"]

    # First run
    key = input("Enter your YouTube data api key: ").strip()
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"api_key": key}, indent=4))
    return key
