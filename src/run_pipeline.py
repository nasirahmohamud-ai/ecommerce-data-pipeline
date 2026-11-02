
import logging
import subprocess
import sys
from pathlib import Path


# 1. Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Create a folder for log files
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"


# 3. Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# 4. Define scripts in execution order
scripts = [
    "create_database.py",
    "clean_data.py",
    "validate_data.py",
    "load_data.py"
]


# 5. Start the pipeline
logger.info("================================")
logger.info("PIPELINE STARTED")
logger.info("================================")


# 6. Run each script
for script in scripts:

    script_path = BASE_DIR / "src" / script

    logger.info("Starting %s", script)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    # 7. Record the script's normal output
    if result.stdout:
        for line in result.stdout.splitlines():
            logger.info("%s", line)

    # 8. Record any error messages
    if result.stderr:
        for line in result.stderr.splitlines():
            logger.error("%s", line)

    # 9. Stop if a script fails
    if result.returncode != 0:
        logger.error("Pipeline failed at %s", script)
        logger.error("PIPELINE FAILED")
        sys.exit(result.returncode)

    logger.info("%s completed successfully", script)


# 10. Finish the pipeline
logger.info("================================")
logger.info("PIPELINE COMPLETED SUCCESSFULLY")
logger.info("================================")
