import unittest
from PyQt5.QtWidgets import QApplication
from gui import WOLApp

class TestWOLApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialise l'application pour les tests."""
        cls.app = QApplication([])

    def setUp(self):
        """Initialise une instance de WOLApp pour chaque test."""
        self.wol_app = WOLApp()

    def test_add_device(self):
        """Test l'ajout d'un périphérique."""
        initial_device_count = len(self.wol_app.devices)
        self.wol_app.save_device("Test Device", "00:11:22:33:44:55", None, None, None)
        self.assertEqual(len(self.wol_app.devices), initial_device_count + 1)

    def test_delete_device(self):
        """Test la suppression d'un périphérique."""
        self.wol_app.save_device("Test Device", "00:11:22:33:44:55", None, None, None)
        initial_device_count = len(self.wol_app.devices)
        self.wol_app.delete_device()
        self.assertEqual(len(self.wol_app.devices), initial_device_count - 1)

    def test_accent_color_change(self):
        """Test le changement de couleur d'accentuation."""
        old_color = self.wol_app.accent_color
        self.wol_app.update_accent_color("#FF5733")
        self.assertNotEqual(self.wol_app.accent_color, old_color)

if __name__ == '__main__':
    unittest.main()
