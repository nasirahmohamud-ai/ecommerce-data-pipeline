
import logging
import subprocess
import sys

from pathlib import Path


# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent


# Create a folder for log files
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Define all scripts in execution order
scripts = [
    "create_database.py",
    "create_warehouse.py",
    "clean_data.py",
    "validate_data.py",
    "load_data.py",
    "load_dates.py",
    "load_warehouse.py"
]


def run_pipeline():

    logger.info("================================")
    logger.info("E-COMMERCE DATA PIPELINE STARTED")
    logger.info("================================")

    # Run each script in order
    for script in scripts:

        script_path = BASE_DIR / "src" / script

        logger.info("Starting %s", script)

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )

        # Record normal output
        if result.stdout:
            for line in result.stdout.splitlines():
                logger.info("%s", line)

        # Record error messages
        if result.stderr:
            for line in result.stderr.splitlines():
                logger.error("%s", line)

        # Stop if a script fails
        if result.returncode != 0:
            logger.error("Pipeline failed at %s", script)
            logger.error("PIPELINE FAILED")
            sys.exit(result.returncode)

        logger.info("%s completed successfully", script)

    # Finish the pipeline
    logger.info("================================")
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("================================")


if __name__ == "__main__":
    run_pipeline()
