"""
GUI Blender wrapper for Session 27 QA import.
"""

import os
import traceback

import bpy


SCRIPT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/06-leaderboard-competition/interior/drafts/qa-session-27.py"
ERROR_FILE = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/06-leaderboard-competition/interior/drafts/session27-qa-error.txt"

try:
    if os.path.exists(ERROR_FILE):
        os.remove(ERROR_FILE)
    with open(SCRIPT, "r") as handle:
        exec(compile(handle.read(), SCRIPT, "exec"), {"__name__": "__main__", "__file__": SCRIPT})
except Exception:
    with open(ERROR_FILE, "w") as handle:
        handle.write(traceback.format_exc())
    raise
finally:
    bpy.ops.wm.quit_blender()
