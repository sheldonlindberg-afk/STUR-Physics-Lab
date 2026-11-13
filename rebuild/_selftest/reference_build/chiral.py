"""Self-test stub for stage chiral: re-exports the reference adapter (not an independent build)."""
from _ref import goldstone_count, sigma_model_vacuum, gmor_mpi, chpt_mpi, yukawa, tensor_identity_residual, goldberger_treiman  # noqa: F401
from _ref import _prov

PROVENANCE = _prov(['goldstone_count', 'sigma_model_vacuum', 'gmor_mpi', 'chpt_mpi', 'yukawa', 'tensor_identity_residual', 'goldberger_treiman'], quoted=['chpt_mpi'])
