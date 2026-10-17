"""Project paths and ingestion settings. All paths are resolved from the repo root."""

from datetime import date
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DIR: Path = DATA_DIR / "raw"
MANUAL_RAW_DIR: Path = RAW_DIR / "manual"
EXPORTS_DIR: Path = DATA_DIR / "exports"
WAREHOUSE_PATH: Path = DATA_DIR / "warehouse.duckdb"

DBT_DIR: Path = PROJECT_ROOT / "dbt"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
FIGURES_DIR: Path = REPORTS_DIR / "figures"

# Analysis scope
SCOPE_START: date = date(2021, 1, 1)
SCOPE_END: date = date(2026, 9, 30)

# Polite-request settings for the PIHPS website
MIN_REQUEST_INTERVAL_SECONDS: float = 2.0
MAX_RETRIES: int = 5
BACKOFF_BASE_SECONDS: float = 2.0
REQUEST_TIMEOUT_SECONDS: float = 30.0
USER_AGENT: str = (
    "food-price-dynamics-id/0.1 (non-commercial data analysis portfolio project; "
    "rate-limited to 1 request per 2 seconds)"
)


def ensure_data_dirs() -> None:
    """Create the local data directories if they do not exist yet."""
    for directory in (RAW_DIR, MANUAL_RAW_DIR, EXPORTS_DIR, FIGURES_DIR):
        directory.mkdir(parents=True, exist_ok=True)
