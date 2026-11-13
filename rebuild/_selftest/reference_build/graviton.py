"""Self-test stub for stage graviton: re-exports the reference adapter (not an independent build)."""
from _ref import point_mass_metric, tpt, ramp_profile, entangling_phase, design_phase  # noqa: F401
from _ref import _prov

PROVENANCE = _prov(['point_mass_metric', 'tpt', 'ramp_profile', 'entangling_phase', 'design_phase'], quoted=[])
