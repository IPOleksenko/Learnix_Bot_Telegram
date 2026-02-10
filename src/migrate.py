from pathlib import Path
from alembic import command
from alembic.config import Config
import sys

# Get the src directory (where this script is located)
BASE_DIR = Path(__file__).resolve().parent

# path to alembic.ini
ALEMBIC_INI_PATH = BASE_DIR / "alembic.ini"

def get_alembic_config() -> Config:
    """Create Alembic config"""
    if not ALEMBIC_INI_PATH.exists():
        raise FileNotFoundError(f"alembic.ini not found at {ALEMBIC_INI_PATH}")

    config = Config(str(ALEMBIC_INI_PATH))
    config.set_main_option("script_location", str(BASE_DIR / "alembic"))
    return config


def upgrade(revision: str = "head"):
    """Apply migrations"""
    try:
        print(f"Applying migration to revision {revision}...")
        command.upgrade(get_alembic_config(), revision)
        print(f"Migration to {revision} applied successfully.")
    except Exception as e:
        print(f"Error applying migration: {e}")
        sys.exit(1)  # Exit with error code


def downgrade(revision: str):
    """Rollback migrations"""
    try:
        if not revision:
            raise ValueError("For downgrade, you must specify --revision")
        print(f"Rolling back to revision {revision}...")
        command.downgrade(get_alembic_config(), revision)
        print(f"Migration rolled back to {revision}.")
    except Exception as e:
        print(f"Error rolling back migration: {e}")
        sys.exit(1)  # Exit with error code


def revision(message: str = None):
    """Create migration (autogenerate)"""
    try:
        print(f"Generating new migration with message: {message}")
        command.revision(
            get_alembic_config(),
            message=message,
            autogenerate=True,
        )
        print(f"Migration {message} created successfully.")
    except Exception as e:
        print(f"Error creating migration: {e}")
        sys.exit(1)  # Exit with error code


def current():
    """Current DB version"""
    try:
        print("Checking current DB version...")
        command.current(get_alembic_config())
    except Exception as e:
        print(f"Error checking current version: {e}")
        sys.exit(1)  # Exit with error code


def history():
    """Migration history"""
    try:
        print("Getting migration history...")
        command.history(get_alembic_config())
    except Exception as e:
        print(f"Error fetching migration history: {e}")
        sys.exit(1)  # Exit with error code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Alembic migrations")

    # Define arguments
    parser.add_argument(
        "command",
        choices=["upgrade", "downgrade", "revision", "current", "history"],
        help="Command to execute",
    )
    parser.add_argument(
        "--message", "-m", help="Migration message for 'revision' command"
    )
    parser.add_argument(
        "--revision", help="Revision (head, base, -1, etc.) for 'upgrade' or 'downgrade'"
    )

    # Parse arguments
    args = parser.parse_args()

    # Call the relevant function based on command
    if args.command == "upgrade":
        upgrade(args.revision or "head")

    elif args.command == "downgrade":
        downgrade(args.revision)

    elif args.command == "revision":
        revision(args.message)

    elif args.command == "current":
        current()

    elif args.command == "history":
        history()
