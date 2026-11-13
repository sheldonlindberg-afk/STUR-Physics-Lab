"""Self-test stub for stage toolkit: re-exports the reference adapter (not an independent build)."""
from _ref import eigvalsh, hessian, exact_derivative, bisect, golden_max, trapezoid, levi_civita  # noqa: F401
from _ref import _prov

PROVENANCE = _prov(['eigvalsh', 'hessian', 'exact_derivative', 'bisect', 'golden_max', 'trapezoid', 'levi_civita'], quoted=[])
