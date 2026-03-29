import os
import shutil
from pathlib import Path

TESTS_TMP = Path(__file__).parent / ".tmp_collaboration"


def pytest_configure(config):
    if TESTS_TMP.exists():
        shutil.rmtree(TESTS_TMP)
    os.environ["COLLABORATION_FILE_DIR"] = str(TESTS_TMP)


def pytest_sessionfinish(session, exitstatus):
    if TESTS_TMP.exists():
        shutil.rmtree(TESTS_TMP)
