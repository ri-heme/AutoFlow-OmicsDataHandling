import sys
import unittest
from unittest.mock import Mock, patch
from types import ModuleType


class TestRdkit(unittest.TestCase):
    @patch.dict(sys.modules, rdkit=None)
    def test_mock(self):
        # Halting correct import of RDKit should produce mocks instead of modules
        from BFAIR.rdkit import Chem, AllChem, Descriptors, Draw
        for mock_module in [Chem, AllChem, Descriptors, Draw]:
            self.assertNotIsInstance(mock_module, ModuleType)
            self.assertIsInstance(mock_module.test, Mock)
            with self.assertRaises(ModuleNotFoundError):
                mock_module.test()

    def test_import(self):
        from BFAIR.rdkit import Chem, AllChem, Descriptors, Draw
        self.assertTrue(all([isinstance(i, ModuleType) for i in [Chem, AllChem, Descriptors, Draw]]))
