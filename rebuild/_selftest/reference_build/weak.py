"""Self-test stub for stage weak: re-exports the reference adapter (not an independent build)."""
from _ref import pion_decay_width, fpi_from_pion_decay  # noqa: F401
from _ref import _prov

PROVENANCE = _prov(['pion_decay_width', 'fpi_from_pion_decay'], quoted=[])
