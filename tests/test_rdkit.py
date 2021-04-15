import unittest
from unittest import mock
from types import ModuleType


class TestRdkit(unittest.TestCase):

    def test_mock(self):
        # Halting correct import of RDKit should produce mocks instead of modules
        with mock.patch.dict("sys.modules", rdkit=None):
            from BFAIR.rdkit import Chem, AllChem, Descriptors, Draw
            for mock_module in [Chem, AllChem, Descriptors, Draw]:
                self.assertNotIsInstance(mock_module, ModuleType)
                with self.assertRaises(ModuleNotFoundError):
                    mock_module.test()

    def test_import(self):
        from BFAIR.rdkit import Chem, AllChem, Descriptors, Draw
        self.assertTrue(all([isinstance(i, ModuleType) for i in [Chem, AllChem, Descriptors, Draw]]))
