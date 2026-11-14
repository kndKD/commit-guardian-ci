"""AI Commit Guardian — thin CLI wrapper around the guardian package.

See guardian/cli.py for flags and exit codes (0 all compliant,
1 any non-compliant, 2 usage error).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from guardian.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
