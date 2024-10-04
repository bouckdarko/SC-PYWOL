
# SC-PYWOL

**SC-PYWOL** est une application Windows avec une interface graphique personnalisable développée en Python. Elle permet d'envoyer des paquets **Wake-On-LAN (WOL)** pour réveiller des périphériques sur un réseau local. L'application offre la gestion de plusieurs périphériques, chacun pouvant avoir un nom, une adresse MAC, une adresse IP optionnelle, ainsi qu'une icône personnalisée.

## Fonctionnalités

- **Envoi de paquets WOL** : Réveillez des périphériques sur votre réseau en utilisant Wake-On-LAN.
- **Gestion des périphériques** :
  - Ajout, modification et suppression de périphériques.
  - Support de l'ajout d'icônes personnalisées pour chaque périphérique.
- **Personnalisation de l'interface** :
  - Ajustement de la taille du texte pour les périphériques.
  - Modification de la couleur d'accentuation, appliquée aux boutons et aux bordures.
  - Icônes SVG colorisées dynamiquement avec la couleur d'accentuation choisie.
- **Fenêtre des paramètres** : Permet de personnaliser la couleur d'accentuation, la couleur du texte, et la taille du texte.
- **Barre de titre personnalisée** : La fenêtre utilise une barre de titre avec des boutons "réduire" et "fermer", ainsi qu'un bouton de paramètres.
- **Redimensionnement intelligent** : Redimensionnez la fenêtre à l'aide d'une icône dédiée en bas à droite.

## Prérequis

- **Python 3.8+**
- **Dépendances Python** :
  - `PyQt5` pour l'interface graphique.
  - `wakeonlan` pour l'envoi des paquets WOL.

Pour installer les dépendances, exécutez la commande suivante :

```bash
pip install -r requirements.txt
```

## Installation

1. Clonez le dépôt ou téléchargez les fichiers sources :

   ```bash
   git clone https://github.com/bouckdarko/SC-PYWOL.git
   ```

2. Accédez au répertoire du projet :

   ```bash
   cd SC-PYWOL
   ```

3. Lancez l'application :

   ```bash
   python gui.py
   ```

## Utilisation

### 1. Ajouter un périphérique

- Cliquez sur **Add Device**.
- Remplissez les champs pour le nom du périphérique, l'adresse MAC et éventuellement l'adresse IP.
- Sélectionnez une icône pour le périphérique à l'aide du bouton **Choose Icon**.
- Cliquez sur **Save Device** pour sauvegarder le périphérique dans la liste.

### 2. Réveiller un périphérique

- Sélectionnez un périphérique dans la liste.
- Le paquet WOL est automatiquement envoyé à l'adresse MAC du périphérique sélectionné.

### 3. Accéder aux paramètres

- Cliquez sur l'icône des paramètres dans la barre de titre.
- Modifiez la taille du texte des périphériques, la couleur d'accentuation et la couleur du texte dans l'interface.
- Les changements sont appliqués en temps réel.

### 4. Supprimer un périphérique

- Sélectionnez un périphérique dans la liste et cliquez sur **Delete Device** pour le retirer.

## Personnalisation

Les paramètres de l'interface et des périphériques sont sauvegardés dans les fichiers JSON suivants :

1. **`settings.json`** : Contient les paramètres de l'interface.
   ```json
   {
     "device_text_size": 12,
     "accent_color": "#4CAF50",
     "text_color": "#FFFFFF"
   }
   ```
   - **device_text_size** : Taille du texte des périphériques.
   - **accent_color** : Couleur d'accentuation de l'interface (boutons, bordures).
   - **text_color** : Couleur du texte dans l'interface.

2. **`devices.json`** : Contient la liste des périphériques ajoutés à l'application.
   ```json
   [
     {
       "name": "Laptop",
       "mac": "00:1F:2G:3H:4I:5J",
       "ip": "192.168.1.11",
       "icon": "path/to/icon.png"
     },
     {
       "name": "Computer",
       "mac": "01:1F:2G:3H:4I:5J",
       "ip": null,
       "icon": "path/to/icon.png"
     }
   ]
   ```

## Contribuer

Les contributions sont les bienvenues ! Si vous trouvez un bug ou souhaitez proposer des améliorations, n'hésitez pas à soumettre une issue ou une pull request.
