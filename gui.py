import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QLabel, QListWidget, QListWidgetItem, QFileDialog, QMainWindow, QDesktopWidget, QColorDialog, QSlider, QGridLayout, QFrame)
from PyQt5.QtGui import QIcon, QCursor, QFont, QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize

# Fichier JSON pour stocker les appareils et les paramètres
DEVICE_FILE = 'devices.json'
SETTINGS_FILE = 'settings.json'

BORDER_WIDTH = 5  # Largeur de la zone cliquable pour redimensionner

class CustomTitleBar(QWidget):
    """Barre de titre personnalisée."""
    def __init__(self, parent, window_to_control=None, show_settings_button=True):
        super().__init__()
        self.parent = parent
        self.window_to_control = window_to_control if window_to_control else parent
        self.start = QPoint(0, 0)

        # Layout de la barre de titre
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Favicon
        favicon = QLabel()
        favicon.setPixmap(QIcon("assets/interface/favicon.png").pixmap(24, 24))

        # Titre de la fenêtre
        self.title_label = QLabel("SC-PYWOL")
        self.title_label.setStyleSheet(f"color: {self.parent.accent_color}; font-size: 16px; padding-left: 10px;")

        # Ajouter la favicon à gauche du titre
        title_bar_layout.addWidget(favicon)
        title_bar_layout.addWidget(self.title_label)

        # Bouton des paramètres (si applicable)
        if show_settings_button:
            self.settings_button = QPushButton(self)
            parameters_icon_path = os.path.abspath("assets/interface/parameters.svg")
            self.settings_button.setIcon(self.colorize_svg(parameters_icon_path, self.parent.accent_color))
            self.settings_button.setFixedSize(30, 30)
            self.settings_button.setStyleSheet("background-color: transparent; color: white;")
            self.settings_button.clicked.connect(self.parent.open_settings)
            title_bar_layout.addStretch()  # Espace avant les boutons à droite
            title_bar_layout.addWidget(self.settings_button)

        # Bouton de minimisation
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet(f"background-color: transparent; color: {self.parent.accent_color};")
        self.minimize_button.clicked.connect(self.minimize_window)

        # Bouton de fermeture
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet(f"background-color: transparent; color: {self.parent.accent_color};")
        self.close_button.clicked.connect(self.close_window)

        # Ajouter les widgets au layout
        title_bar_layout.addWidget(self.minimize_button)
        title_bar_layout.addWidget(self.close_button)

        self.setLayout(title_bar_layout)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #333;")  # Couleur de fond de la barre de titre

    def minimize_window(self):
        """Minimiser la fenêtre."""
        self.window_to_control.showMinimized()

    def close_window(self):
        """Fermer la fenêtre."""
        self.window_to_control.close()

    def mousePressEvent(self, event):
        """Gérer le déplacement de la fenêtre."""
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True

    def mouseMoveEvent(self, event):
        """Déplacer la fenêtre avec la souris."""
        if event.buttons() == Qt.LeftButton:
            self.window_to_control.move(self.window_to_control.pos() + event.globalPos() - self.start)
            self.start = event.globalPos()

    def colorize_svg(self, icon_path, color):
        """Colorier les icônes SVG avec la couleur d'accentuation."""
        pixmap = QPixmap(icon_path)
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color))
        painter.end()
        return QIcon(pixmap)

    def update_colors(self):
        """Mettre à jour la couleur des éléments dans la barre de titre."""
        self.title_label.setStyleSheet(f"color: {self.parent.accent_color};")
        self.minimize_button.setStyleSheet(f"color: {self.parent.accent_color};")
        self.close_button.setStyleSheet(f"color: {self.parent.accent_color};")


class SettingsWindow(QWidget):
    """Fenêtre des paramètres."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Paramètres")
        self.setGeometry(200, 200, 400, 300)

        # Utiliser la barre de titre personnalisée
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.title_bar = CustomTitleBar(self.parent, window_to_control=self, show_settings_button=False)

        layout = QVBoxLayout()

        # Section pour la taille du texte
        text_size_layout = QVBoxLayout()
        text_size_label = QLabel("Taille du texte des périphériques :", self)
        text_size_layout.addWidget(text_size_label)

        self.text_size_slider = QSlider(Qt.Horizontal, self)
        self.text_size_slider.setMinimum(8)
        self.text_size_slider.setMaximum(32)
        self.text_size_slider.setValue(self.parent.device_text_size)  # Taille actuelle
        self.text_size_slider.valueChanged.connect(self.change_text_size)
        text_size_layout.addWidget(self.text_size_slider)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        text_size_layout.addWidget(separator)

        # Section pour la couleur d'accentuation
        color_layout = QVBoxLayout()
        color_label = QLabel("Couleur d'accentuation :", self)
        color_layout.addWidget(color_label)

        self.color_button = QPushButton("Changer la couleur d'accentuation", self)
        self.color_button.setStyleSheet(f"background-color: {self.parent.accent_color}; color: white;")
        self.color_button.clicked.connect(self.change_accent_color)
        color_layout.addWidget(self.color_button)

        layout.addLayout(text_size_layout)
        layout.addLayout(color_layout)

        # Séparateur pour les couleurs d'interface
        separator_interface = QFrame()
        separator_interface.setFrameShape(QFrame.HLine)
        separator_interface.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator_interface)

        # Section pour la couleur du texte
        text_color_layout = QVBoxLayout()
        text_color_label = QLabel("Couleur du texte :", self)
        text_color_layout.addWidget(text_color_label)

        self.text_color_button = QPushButton("Changer la couleur du texte", self)
        self.text_color_button.setStyleSheet(f"background-color: {self.parent.accent_color}; color: white;")
        self.text_color_button.clicked.connect(self.change_text_color)
        text_color_layout.addWidget(self.text_color_button)

        layout.addLayout(text_color_layout)

        # Layout principal incluant la barre de titre
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_bar)  # Ajouter la barre de titre
        main_layout.addLayout(layout)
        self.setLayout(main_layout)

    def change_text_size(self):
        """Changer la taille du texte des périphériques."""
        size = self.text_size_slider.value()
        self.parent.update_device_text_size(size)

    def change_accent_color(self):
        """Changer la couleur d'accentuation."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent.update_accent_color(color.name())
            self.update_button_colors()  # Appliquer immédiatement
            self.title_bar.update_colors()  # Mettre à jour la barre de titre des paramètres

    def change_text_color(self):
        """Changer la couleur du texte."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent.update_text_color(color.name())

    def update_button_colors(self):
        """Mettre à jour la couleur des boutons dans les paramètres."""
        self.color_button.setStyleSheet(f"background-color: {self.parent.accent_color}; color: white;")
        self.text_color_button.setStyleSheet(f"background-color: {self.parent.accent_color}; color: white;")


class WOLApp(QMainWindow):
    """Fenêtre principale avec redimensionnement."""
    def __init__(self):
        super().__init__()
        self.devices = []
        self.setMouseTracking(True)
        self.resizing = False
        self.mouse_pressed = False
        self.mouse_pos = None
        self.device_text_size = 12  # Taille du texte par défaut
        self.accent_color = "#4CAF50"  # Couleur d'accentuation par défaut (vert)
        self.text_color = "#ffffff"  # Couleur du texte par défaut

        self.load_settings()

        # Masquer la barre de titre par défaut
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Titre de la fenêtre dans la barre des tâches
        self.setWindowTitle("PYWOL")

        # Adapter la taille de la fenêtre à la moitié de l'écran de l'utilisateur
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(screen_geometry.width() // 4, screen_geometry.height() // 4,
                         screen_geometry.width() // 2, screen_geometry.height() // 2)

        # Créer la barre de titre personnalisée
        self.title_bar = CustomTitleBar(self)

        # Contenu principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Liste des périphériques
        self.device_list = QListWidget(self)
        self.load_devices()
        main_layout.addWidget(self.device_list)

        # Bouton pour ajouter un nouvel appareil
        add_button = QPushButton('Add Device', self)
        add_button.clicked.connect(self.add_device_dialog)
        main_layout.addWidget(add_button)

        # Bouton pour supprimer un appareil
        delete_button = QPushButton('Delete Device', self)
        delete_button.clicked.connect(self.delete_device)
        main_layout.addWidget(delete_button)

        # Icône en bas à droite pour indiquer le redimensionnement
        self.resize_icon = QPushButton(self)
        icon_path = os.path.abspath("assets/interface/resize_icon.svg")
        self.resize_icon.setIcon(self.colorize_svg(icon_path, self.accent_color))
        self.resize_icon.setFixedSize(20, 20)
        self.resize_icon.setStyleSheet(f"background-color: transparent; border: 1px solid {self.accent_color};")
        self.resize_icon.setCursor(QCursor(Qt.SizeFDiagCursor))
        resize_icon_layout = QHBoxLayout()
        resize_icon_layout.addStretch()
        resize_icon_layout.addWidget(self.resize_icon)
        main_layout.addLayout(resize_icon_layout)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.title_bar)  # Ajouter la barre de titre personnalisée
        layout.addLayout(main_layout)

        # Configuration du widget principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connecter l'icône à l'événement de redimensionnement
        self.resize_icon.mousePressEvent = self.start_resize

        # Charger et appliquer les paramètres
        self.apply_accent_color()

        # Ajouter la favicon
        self.setWindowIcon(QIcon("assets/interface/favicon.png"))

    def load_devices(self):
        """Charger les périphériques depuis le fichier JSON."""
        if os.path.exists(DEVICE_FILE):
            with open(DEVICE_FILE, 'r') as f:
                self.devices = json.load(f)

            self.device_list.clear()
            for device in self.devices:
                self.add_device_to_list(device)

    def add_device_to_list(self, device):
        """Ajouter un appareil à la liste affichée."""
        item = QListWidgetItem(f"{device['name']} ({device['mac']})")
        if device['icon'] and os.path.exists(device['icon']):
            icon = QIcon(device['icon'])
            # Redimensionner l'icône en fonction de la taille du texte
            pixmap = icon.pixmap(QSize(self.device_text_size * 2, self.device_text_size * 2))
            item.setIcon(QIcon(pixmap))
        item.setFont(QFont("Arial", self.device_text_size))
        # Ajuster la taille de l'icône
        item.setSizeHint(QSize(self.device_text_size * 3, self.device_text_size * 3))
        self.device_list.addItem(item)

    def add_device_dialog(self):
        """Afficher une boîte de dialogue pour ajouter un nouvel appareil."""
        add_window = QWidget()
        add_window.setWindowTitle('Add New Device')
        add_layout = QVBoxLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Device Name")
        mac_input = QLineEdit()
        mac_input.setPlaceholderText("MAC Address")
        ip_input = QLineEdit()
        ip_input.setPlaceholderText("IP Address (optional)")

        # Rendre icon_path un attribut de add_window pour éviter qu'il soit supprimé
        add_window.icon_path = QLineEdit()  
        icon_button = QPushButton('Choose Icon')

        def choose_icon():
            icon_file, _ = QFileDialog.getOpenFileName(self, 'Choose Icon', '', 'Images (*.png *.xpm *.jpg)')
            add_window.icon_path.setText(icon_file)

        icon_button.clicked.connect(choose_icon)

        save_button = QPushButton('Save Device')
        save_button.clicked.connect(lambda: self.save_device(
            name_input.text(), mac_input.text(), ip_input.text(), add_window.icon_path.text(), add_window))

        add_layout.addWidget(QLabel("Device Name:"))
        add_layout.addWidget(name_input)
        add_layout.addWidget(QLabel("MAC Address:"))
        add_layout.addWidget(mac_input)
        add_layout.addWidget(QLabel("IP Address (optional):"))
        add_layout.addWidget(ip_input)
        add_layout.addWidget(icon_button)
        add_layout.addWidget(add_window.icon_path)
        add_layout.addWidget(save_button)

        add_window.setLayout(add_layout)
        add_window.show()

    def save_device(self, name, mac, ip, icon, window):
        """Sauvegarder un nouvel appareil."""
        device = {
            "name": name,
            "mac": mac,
            "ip": ip if ip else None,
            "icon": icon if icon else None
        }
        self.devices.append(device)
        self.add_device_to_list(device)
        self.save_devices_to_file()
        window.close()

    def save_devices_to_file(self):
        """Sauvegarder les appareils dans le fichier JSON."""
        with open(DEVICE_FILE, 'w') as f:
            json.dump(self.devices, f, indent=4)

    def delete_device(self):
        """Supprimer un appareil sélectionné."""
        selected_item = self.device_list.currentRow()
        if selected_item >= 0:
            del self.devices[selected_item]
            self.device_list.takeItem(selected_item)
            self.save_devices_to_file()
            print("Device deleted.")

    def wake_from_mac_input(self):
        """Envoyer un paquet WOL à l'adresse MAC entrée manuellement."""
        mac_address = self.mac_input.text()
        if mac_address:
            wake_device(mac_address)
            print(f"Magic packet sent to {mac_address}")
        else:
            print("Please enter a valid MAC address.")

    def open_settings(self):
        """Ouvrir la fenêtre des paramètres."""
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def update_device_text_size(self, size):
        """Mettre à jour la taille du texte des périphériques."""
        self.device_text_size = size
        self.load_devices()  # Recharger les appareils avec la nouvelle taille de texte
        self.save_settings()

    def update_accent_color(self, color):
        """Mettre à jour la couleur d'accentuation."""
        self.accent_color = color
        self.apply_accent_color()  # Mettre à jour l'interface immédiatement
        self.refresh_icons()       # Rafraîchir les icônes SVG
        self.save_settings()

    def update_text_color(self, color):
        """Mettre à jour la couleur du texte."""
        self.text_color = color
        self.apply_accent_color()  # Rafraîchir l'interface avec la nouvelle couleur de texte
        self.save_settings()

    def apply_accent_color(self):
        """Appliquer la couleur d'accentuation."""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: {self.text_color};
                border: 1px solid {self.accent_color};
                padding: 10px;
                font-size: 14px;
            }}
            QLineEdit, QListWidget {{
                border: 1px solid {self.accent_color};
                color: {self.text_color};
            }}
            QPushButton:hover {{
                background-color: {self.accent_color};
            }}
            QLabel {{
                color: {self.text_color};
            }}
        """)
        # Appliquer la couleur d'accentuation au bouton des paramètres si la fenêtre est ouverte
        if hasattr(self, 'settings_window') and self.settings_window is not None:
            self.settings_window.update_button_colors()
        
        # Mettre à jour les couleurs de la barre de titre
        self.title_bar.update_colors()

        # Mettre à jour l'icône de redimensionnement
        self.resize_icon.setStyleSheet(f"background-color: transparent; border: 1px solid {self.accent_color};")

    def refresh_icons(self):
        """Rafraîchir les icônes avec la couleur d'accentuation."""
        parameters_icon_path = os.path.abspath("assets/interface/parameters.svg")
        icon_path = os.path.abspath("assets/interface/resize_icon.svg")

        # Rafraîchir les icônes SVG en fonction de la nouvelle couleur d'accentuation
        self.title_bar.settings_button.setIcon(self.colorize_svg(parameters_icon_path, self.accent_color))
        self.resize_icon.setIcon(self.colorize_svg(icon_path, self.accent_color))

    def colorize_svg(self, icon_path, color):
        """Colorier les icônes SVG avec la couleur d'accentuation."""
        pixmap = QPixmap(icon_path)
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color))
        painter.end()
        return QIcon(pixmap)

    def start_resize(self, event):
        """Débuter le redimensionnement en cliquant sur l'icône."""
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.mouse_pos = event.globalPos()
            self.resizing = True

    def mouseMoveEvent(self, event):
        """Redimensionner la fenêtre si le redimensionnement est actif."""
        if self.resizing:
            delta = event.globalPos() - self.mouse_pos
            self.resize(self.width() + delta.x(), self.height() + delta.y())
            self.mouse_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        """Réinitialiser l'état du redimensionnement."""
        self.resizing = False
        self.mouse_pressed = False

    def load_settings(self):
        """Charger les paramètres depuis settings.json"""
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            self.device_text_size = settings.get("device_text_size", 12)
            self.accent_color = settings.get("accent_color", "#4CAF50")
            self.text_color = settings.get("text_color", "#ffffff")

    def save_settings(self):
        """Sauvegarder les paramètres dans settings.json"""
        settings = {
            "device_text_size": self.device_text_size,
            "accent_color": self.accent_color,
            "text_color": self.text_color
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Charger et appliquer le style QSS (si disponible)
    if os.path.exists("style.qss"):
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())

    ex = WOLApp()
    ex.show()
    sys.exit(app.exec_())
