"""Self-test stub for stage photon: re-exports the reference adapter (not an independent build)."""
from _ref import vacuum_polarization, dalpha_lep, alpha0_inv  # noqa: F401
from _ref import _prov

PROVENANCE = _prov(['vacuum_polarization', 'dalpha_lep', 'alpha0_inv'], quoted=[])
