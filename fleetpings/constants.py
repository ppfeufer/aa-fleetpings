"""
Constants
"""

# Standard Library
import os

APP_NAME = "aa-fleetpings"
PACKAGE_NAME = "fleetpings"
GITHUB_URL = f"https://github.com/ppfeufer/{APP_NAME}"

DISCORD_WEBHOOK_REGEX = r"https:\/\/discord\.com\/api\/webhooks\/[\d]+\/[a-zA-Z0-9_-]+$"

APP_BASE_DIR = os.path.join(os.path.dirname(__file__))
APP_STATIC_DIR = os.path.join(APP_BASE_DIR, "static", PACKAGE_NAME)
