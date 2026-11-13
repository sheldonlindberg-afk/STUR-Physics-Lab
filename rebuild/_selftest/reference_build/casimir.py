"""Self-test stub for stage casimir: re-exports the reference adapter (not an independent build)."""
from _ref import sphere_K, green_tensor, cp_integral, cp_energy, diamond_radius, casimir_safe_gap  # noqa: F401
from _ref import _prov

PROVENANCE = _prov(['sphere_K', 'green_tensor', 'cp_integral', 'cp_energy', 'diamond_radius', 'casimir_safe_gap'], quoted=['cp_energy'])
