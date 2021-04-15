"""RDKit module.

This module centralizes RDKit dependency. If RDKit is not installed, a mock module (that raises exceptions on every
function call) will be supplied. This renders RDKit an optional dependency, that is only required if certain functions
are called."""

__all__ = ["Chem", "AllChem", "Descriptors", "Draw"]

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, Draw
except ModuleNotFoundError:
    from unittest.mock import Mock

    class _MockModule:
        # A class that mocks a RDKit module. Every method call raises an exception.
        def __getattr__(self, _):
            mock = Mock()
            mock.side_effect = ModuleNotFoundError("Requires rdkit.")
            return mock

    Chem, AllChem, Descriptors, Draw = [_MockModule()] * 4
