"""Chemins des fichiers de données — module léger sans dépendances circulaires."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "users_labeled_manual.csv"
AGGREGATED_DATA_FILE = ROOT / "users_aggregated.csv"

__all__ = ["ROOT", "DATA_FILE", "AGGREGATED_DATA_FILE"]
