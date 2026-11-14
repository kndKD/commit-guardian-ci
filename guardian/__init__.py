"""AI Commit Guardian package — scoring, suggestions, CLI and LLM layer."""

from guardian.scoring import check
from guardian.suggest import suggest

__all__ = ["check", "suggest"]
