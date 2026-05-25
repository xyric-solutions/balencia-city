"""
GUI Blender wrapper for Session 39.

Used when background Blender crashes on startup or MCP drops its connection.
Writes an error file if the build script fails, then asks Blender to quit after
artifacts are produced.
"""

import os
import traceback

import bpy


SCRIPT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/09-recovery-sleep/interior/drafts/build-session-39.py"
ERROR_FILE = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/09-recovery-sleep/interior/drafts/session39-run-error.txt"

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
