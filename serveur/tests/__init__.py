import os
import tempfile

if "STATE_DIRECTORY" not in os.environ:
    os.environ["STATE_DIRECTORY"] = tempfile.mkdtemp()
