"""Compatibility wrapper for the Cafe24 skin analyzer.

The implementation lives in ``mcp/backends/skin_analyzer.py`` because existing
release-channel updaters copy the whole ``mcp/backends`` directory. Keeping this
wrapper preserves direct ``from skin_analyzer import ...`` imports for source
checkouts and fresh release zips.
"""

from backends.skin_analyzer import *  # noqa: F401,F403
