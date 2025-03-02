"""
Constants
"""

# Standard Library
import os

APP_NAME = "aa-fleetpings"
PACKAGE_NAME = "fleetpings"
GITHUB_URL = f"https://github.com/ppfeufer/{APP_NAME}"

DISCORD_WEBHOOK_REGEX = r"https:\/\/discord\.com\/api\/webhooks\/[\d]+\/[a-zA-Z0-9_-]+$"

AA_FLEETPINGS_BASE_DIR = os.path.join(os.path.dirname(__file__))
AA_FLEETPINGS_STATIC_DIR = os.path.join(AA_FLEETPINGS_BASE_DIR, "static", PACKAGE_NAME)
