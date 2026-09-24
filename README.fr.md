<p align="center">
  <img src="https://raw.githubusercontent.com/Faycall1l/Ashiart/main/docs/images/logo.svg" width="640" alt="Logo AshiArt : seize cellules ambre passant du plein au vide sur fond presque noir" />
</p>

<h1 align="center">AshiArt</h1>

<p align="center">
  Convertissez des images en art ASCII depuis le terminal ou Python.
  Texte brut, vraies couleurs ANSI et export HTML préservant les couleurs.
</p>

<p align="center">
  <a href="https://pypi.org/project/ashiart/"><img src="https://img.shields.io/pypi/v/ashiart" alt="Version PyPI" /></a>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+" />
  <a href="https://github.com/Faycall1l/Ashiart/actions"><img src="https://github.com/Faycall1l/Ashiart/actions/workflows/python-package.yml/badge.svg" alt="État de compilation" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="Licence MIT" /></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/ashiart/"><img src="https://img.shields.io/pypi/dm/ashiart" alt="Téléchargements mensuels" /></a>
  <img src="https://img.shields.io/github/last-commit/Faycall1l/Ashiart" alt="Dernier commit" />
</p>

> Version française. L'original faisant foi est
> [README.md](README.md) ; les exemples de code sont inchangés.

## Sommaire

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Démarrage rapide](#démarrage-rapide)
- [Référence de la ligne de commande](#référence-de-la-ligne-de-commande)
- [API Python](#api-python)
- [Modes de rendu](#modes-de-rendu)
- [Table de caractères](#table-de-caractères)
- [Fonctionnement](#fonctionnement)
- [Animation](#animation)
- [Galerie](#galerie)
- [Exemples](#exemples)
- [Structure du projet](#structure-du-projet)
- [Développement](#développement)
- [Contribution](#contribution)
- [Remerciements](#remerciements)
- [Licence](#licence)

## Aperçu

AshiArt convertit les images en grilles de caractères pour les terminaux,
les documents en texte brut et les pages HTML préservant les couleurs.
Chaque cellule encode la luminosité — et optionnellement la direction des
contours — de ses pixels sources.

Décode tous les formats d'image supportés par Pillow, dont JPEG, PNG, BMP,
GIF et WebP — depuis un chemin local ou directement depuis une URL http(s).

Exemple de sortie (`docs/images/puppy.jpg`, largeur 60, mode standard avec
surimpression de contours — tracés selon l'orientation de Sobel) :

```text
%%*??*+++;::,.,. .     .,:, . ..,,,.....,,,.:;:;;;+*???%%S##
%?*++;;::,::,..----------------/   ----%+,:;+;::;;:::;+**?%%
?*+;;;::,,,,.\\---@@@@@@@@@@@--------@S+,::;;*;++;++;;++***?
**+;::,     \\@@@@@@#@@####S##@@--@@#SS-----::+*;:::;+***??%
;;:,,...   \\@@@@@@######%##SSS@@@@@###@@@@-//,:,,::;++*+**?
*+;;;;:::,\\@@@@@####S##S#@S%%SSSS###@@@@#@@@|,,,:;;;;;;+***
%*++;;:,, ||@@@@##S#SSS%SS##%%%%%SSSS#@@@@@@#|:;;;;;;+;+;+**
*+++;,,,, ||@@@@####S###%S#@S%S@#S@S##%#@@@@||;:::;::::;:;+?
+:;::,..,.//@@@@#SS###S#S#@@S%+%#SS%S#SS@@@#S+;;:;;++;;;:;;+
;:,,,.... ///##@##SS##%SSS@#@S+?%S%S#@@@@@\*******+?*****??*
:::::,..   //@###@####S#@#@@#@SS%%SS##@@@?*+***+++++*+****?%
;;;::,,...,.///####@###S#@@@@#@#%S#SS##@#?**++++;;;;+***?%%%
?*;,,,..,,.,.//--@@@#S#########S%S?%S##@@S%?*+*+++++++*????%
;;;::::::,,....-------%%#####@#%??%#@#@@\\++++*+**+****????%
;:::,,,:,.,,....  ---//SSSSS#@@@######S\\:;:;++++****????%??
*+**+;:,,,.,.,,,,.... //##@#@#@@##@@@@\\,:,:;;;;;;+;*?++%SSS
????*+;::;:,,,,,,,,... //S#@@@@#\-----\:::::;+;;+*%%%%?%%SSS
S%%%?**+**++;;:::,,,,,:,//#@@@@|\,---.,,,,,:::;+***??%%%%%S#
SS%%???*++++;;:;;::,,:::,/@#@@@\| ,.,,,,,,,:,,:;+**?%%%%SSS#
SSS%%??****++;+;;;;::::::;*?%%?;;::;;;++;;+++++**??%SSSSSS##
```

```bash
ashiart docs/images/puppy.jpg --width 60 --edges --edge-threshold 0.5
```

Photo : chiot noir via Lorem Picsum (id 237, licence Unsplash).
Un pelage sombre sur des planches claires est le profil d'entrée que
l'ASCII restitue le plus fidèlement : contraste élevé, sujet unique,
contours nets.

Le gros plan sur la chouette (`docs/images/owl-face.jpg`, largeur 70)
teste plutôt les détails fins. Le mode dense (69 niveaux) le rend le
mieux — essayez :

```bash
ashiart docs/images/owl-face.jpg --width 70 --mode dense
```

Sortie terminal en vraies couleurs (`docs/images/puppy-head.jpg`, mode
dense, `--color`), restituée ici en image car Markdown ne peut pas
afficher l'ANSI :

<p align="center">
  <img src="https://raw.githubusercontent.com/Faycall1l/Ashiart/main/docs/images/color-preview.png" width="630" alt="Art ASCII en vraies couleurs d'une tête de chiot noir" />
</p>

```bash
ashiart docs/images/puppy-head.jpg --width 70 --mode dense --color
```

## Fonctionnalités

- Conversion image-vers-ASCII avec largeur explicite, ou hauteur proportionnelle
- Quatre modes de rendu : standard, dense, blocks, braille
- Surimpression de contours Sobel : les contours forts deviennent des glyphes directionnels `- / | \`
- Sortie terminal en vraies couleurs ANSI, couleur par cellule échantillonnée après enhancement
- Export HTML préservant les couleurs, taille de police configurable
- Réglages tonaux : contraste, luminosité, netteté, gamma, autocontraste
  (étirement des niveaux, activé par défaut), égalisation locale CLAHE,
  accentuation des détails par différence de gaussiennes, tramage, inversion
- Tables de caractères personnalisées, ordonnées du plus sombre au plus clair
- Interface en ligne de commande et API Python importable
- Multiplateforme : macOS, Linux et Windows

## Prérequis

- Python 3.8 ou supérieur
- Pillow 10 ou supérieur
- NumPy 1.20 ou supérieur

## Installation

Depuis PyPI :

```bash
pip install ashiart
```

Depuis les sources :

```bash
git clone https://github.com/Faycall1l/Ashiart.git
cd Ashiart
pip install .
```

Installation de développement :

```bash
pip install -e .
pip install pytest
```

## Démarrage rapide

Afficher l'art ASCII dans le terminal :

```bash
ashiart docs/images/sample.jpg --width 80
```

Aucun fichier local requis — les URL se téléchargent à la volée :

```bash
ashiart https://picsum.photos/id/237/1200/800 --width 80
```

Rien sous la main — restituez l'image de calibration intégrée :

```bash
ashiart --demo --width 80
```

Enregistrer la sortie texte et un rendu HTML couleur en une passe :

```bash
ashiart docs/images/sample.jpg \
  --width 80 \
  --mode dense \
  --contrast 1.3 \
  --edge-enhance \
  --output output.txt \
  --html output.html
```

Sortie terminal colorisée avec caractères blocs :

```bash
ashiart docs/images/sample.jpg --mode blocks --color --width 100
```

Usage Python minimal :

```python
from ashiart import image_to_ascii

art = image_to_ascii("docs/images/sample.jpg", width=80)
print(art)
```

## Référence de la ligne de commande

| Option | Défaut | Description |
| --- | --- | --- |
| `image_path` | requis | Chemin local, URL http(s), `-` pour stdin ; omettre avec `--demo` |
| `--demo` | off | Restitue l'image de calibration intégrée |
| `-o, --output` | console | Fichier de sortie texte ; affiche sur stdout si omis |
| `-w, --width` | largeur tty, sinon `100` | Largeur de sortie en caractères |
| `-H, --height` | proportionnelle | Hauteur de sortie en caractères |
| `-c, --chars` | table intégrée | Caractères personnalisés, du plus sombre au plus clair |
| `-m, --mode` | `standard` | `standard`, `dense`, `blocks` ou `braille` |
| `--contrast` | `1.0` | Multiplicateur de contraste |
| `--brightness` | `1.0` | Multiplicateur de luminosité |
| `--sharpness` | `1.0` | Multiplicateur de netteté |
| `--gamma` | `1.0` | Exposant de courbe tonale, >1 assombrit les tons moyens |
| `--resample` | `lanczos` | Filtre de sous-échantillonnage : `lanczos` ou `box` (moyenne locale) |
| `--edge-enhance` | off | Filtre PIL de renforcement des contours avant transcodage |
| `--edges` | off | Surimpression Sobel : contours en glyphes `- / | \` |
| `--edge-threshold` | `0.35` | Seuil de magnitude Sobel normalisée pour `--edges` |
| `--no-autocontrast` | off | Désactive l'étirement automatique des niveaux |
| `--dithering` | off | Applique un tramage pour la texture |
| `--clahe` | off | Égalisation locale du contraste pour les photos plates |
| `--dog` | off | Accentuation DoG : `--dog SMALL LARGE AMPLIFY` |
| `--invert` | off | Inverse le transcodage des luminosités |
| `--color` | off | Émet des codes d'échappement ANSI en vraies couleurs |
| `--play` | off | Joue une entrée GIF/vidéo en animation ASCII bouclée |
| `--webcam` | off | ASCII en direct depuis une webcam (défaut : 0, Ctrl-C arrête) |
| `--loop` | `0` | Nombre de boucles d'animation, 0 boucle sans fin |
| `--max-fps` | `30` | Plafond d'images par seconde pour l'animation |
| `--html PATH` | none | Écrit aussi un rendu HTML couleur vers `PATH` |
| `--bg` | `black` | Fond de page HTML : `black` ou `white` |
| `--open` | off | Ouvre la sortie `--html` dans un navigateur (requiert `--html`) |
| `--font-size` | `8` | Taille de police HTML en pixels |

Aide complète :

```bash
ashiart --help
```

## API Python

Générateur de base :

```python
from ashiart import AsciiArtGenerator, image_to_ascii

generator = AsciiArtGenerator(width=80)
art = generator.generate_from_image("docs/images/sample.jpg")
generator.save_to_file(art, "output.txt")

# Variante ANSI en vraies couleurs
color_art = generator.generate_from_image("docs/images/sample.jpg", color=True)
```

Générateur avancé :

```python
from ashiart import (
    EnhancedAsciiArtGenerator,
    image_to_ascii,
    image_to_html_ascii,
)

generator = EnhancedAsciiArtGenerator(width=80, mode="dense")
generator.set_enhancement(contrast=1.4, brightness=1.05, edge_enhance=True)
art = generator.generate_from_image("docs/images/sample.jpg")

# Sortie ANSI en vraies couleurs
color_art = generator.generate_from_image("docs/images/sample.jpg", ansi=True)

# Sortie HTML aux couleurs d'origine
html = generator.generate_html(
    "docs/images/sample.jpg",
    preserve_color=True,
    font_size=8,
)
generator.save_html_to_file(html, "output.html")

# Fonctions utilitaires (un seul point d'entrée texte + HTML)
art = image_to_ascii(
    "docs/images/sample.jpg",
    width=80,
    mode="dense",
    contrast=1.3,
    edge_enhance=True,
)
html = image_to_html_ascii("docs/images/sample.jpg", width=80)
```

## Modes de rendu

| Mode | Jeu de caractères | Idéal pour |
| --- | --- | --- |
| `standard` | Table ASCII à 12 niveaux | Sortie terminal lisible |
| `dense` | Table mesurée à 69 niveaux | Dégradés lisses, détail photographique |
| `blocks` | Table de blocs à 5 niveaux (`█▓▒░ `) | Rendu géométrique à fort contraste |
| `braille` | 256 motifs de points, 2×4 points par cellule | Résolution effective ~4× |

## Table de caractères

La table par défaut est strictement ordonnée du plus sombre au plus
clair. Elle se termine par une espace, pour que le blanc pur rende du
papier vierge au lieu d'un point :

```text
@ # S % ? * + ; : , . (espace)
```

Le logo de l'en-tête exprime la même idée géométriquement : une grille
de cellules passant du plein au vide, c'est-à-dire la luminosité
traduite en encre.
Les tables personnalisées doivent préserver l'ordre sombre-vers-clair,
par exemple :

```bash
ashiart input.jpg --chars "@%*+=-:. "
```

## Fonctionnement

Chaque cellule de sortie correspond à exactement un pixel rééchantillonné
(le braille regroupe un bloc 2×4 par cellule). Le pipeline, dans l'ordre :

0. **Chargement.** Décodage depuis un chemin local ou une URL http(s),
   application de l'orientation EXIF pour redresser les photos de
   téléphone, et fusion de la transparence sur blanc.
1. **Rééchantillonnage.** Sous-échantillonnage LANCZOS (`--resample box`
   bascule sur la moyenne locale) vers `width` colonnes. Les lignes
   valent par défaut `hauteur × width / largeur_image × 0,5`, compensant
   le rapport ~2:1 hauteur-largeur des glyphes monospace ; `--height`
   le surcharge.
2. **Enhancement.** Multiplicateurs de contraste, luminosité, netteté et
   gamma, accentuation des détails par différence de gaussiennes, puis
   filtre de renforcement des contours et inversion optionnelle. Tout
   est neutre par défaut.
3. **Niveaux de gris.** Mode `L` de PIL (luma ITU-R BT.601).
   L'autocontraste, activé par défaut, étire la plage utilisée vers
   0–255 avec un seuil de 1 % ; l'option CLAHE égalise ensuite le
   contraste local tuile par tuile.
4. **Champ de contours (optionnel, `--edges`).** Gradients de Sobel 3×3
   par cellule, magnitude normalisée par le pic de l'image. Les cellules
   au seuil ou au-delà (`--edge-threshold`, défaut 0,35) prennent un
   glyphe de contour selon la direction du gradient tournée de 90° et
   repliée dans [0°, 180°) :

   | Direction du contour | Glyphe | Plage d'angles |
   | --- | --- | --- |
   | Horizontale | `-` | [0°, 22,5°) ∪ [157,5°, 180°) |
   | Diagonale | `/` | [22,5°, 67,5°) |
   | Verticale | `\|` | [67,5°, 112,5°) |
   | Diagonale | `\` | [112,5°, 157,5°) |

   Les autres cellules gardent leur caractère tonal. Ignoré en mode braille.
5. **Transcodage.** `index = round(L / 255 × (N−1))`, borné à la table.
   L'arrondi (et non la troncature) donne à chaque caractère un seau de
   luminosité symétrique. Les cellules braille seuillent chacun de leurs
   8 points à 128.
6. **Émission.** Texte brut, premier plan ANSI en vraies couleurs par
   cellule, ou éléments HTML `<span>` préservant la couleur par cellule
   après enhancement.

## Animation

Les GIF se jouent image par image à leurs durées natives ; les fichiers
vidéo (mp4, avi, mov, mkv, webm) se décodent via OpenCV (`pip install
ashiart[video]`) ; `--webcam` diffuse une caméra en direct. Tous les
modes, enhancements et `--color` s'appliquent par image.

<p align="center">
  <img src="https://raw.githubusercontent.com/Faycall1l/Ashiart/main/docs/images/demo.gif" width="360" alt="Balle ambre glissant sur une grille sombre, source de la démo d'animation" />
</p>

```bash
# Boucler un GIF dans le terminal (Ctrl-C arrête)
ashiart docs/images/demo.gif --play --width 60

# Deux boucles, puis sortie
ashiart docs/images/demo.gif --play --loop 2 --width 60

# Un fichier vidéo (requiert l'extra vidéo)
ashiart movie.mp4 --play --width 100

# Webcam en direct, vue miroir selfie
ashiart --webcam --width 100 --color

# Exporter l'animation en page HTML bouclée autonome
ashiart docs/images/demo.gif --play --loop 1 --html animation.html
```

## Galerie

Source (`docs/images/puppy-head.jpg`, 700×600) :

<p align="center">
  <img src="https://raw.githubusercontent.com/Faycall1l/Ashiart/main/docs/images/puppy-head.jpg" width="240" alt="Photo source de tête de chiot noir" />
</p>

Voir le [README anglais](README.md#gallery) pour les trois rendus
commentés (les blocs ASCII y sont vérifiés à l'octet près).

## Exemples

- `examples/basic_usage.py` : conversion minimale et tables personnalisées
- `examples/enhanced_demo.py` : modes, enhancements et export HTML

Lancer l'exemple de base :

```bash
python examples/basic_usage.py docs/images/sample.jpg
```

## Structure du projet

```text
ashiart/
  __init__.py      Exports publics : générateurs, image_to_ascii, helper HTML
  generator.py     Convertisseur mono-table sans NumPy, avec support ANSI
  enhanced.py      Modes, enhancements, surimpression de contours Sobel, HTML, ANSI
  cli.py           Interface en ligne de commande (tous les flags dans un parser)
test/
  test_generator.py
  test_enhanced.py
  test_cli.py
docs/images/
  logo.svg           Logo du projet et référence de la table
  sample.jpg         Entrée d'exemple utilisée dans les snippets
  puppy.jpg          Échantillon contrasté du README
  puppy-head.jpg     Recadrage serré pour la démo couleur
  owl-face.jpg       Recadrage serré pour les démos détaillées
  color-preview.png  Aperçu en vraies couleurs montré ci-dessus
examples/
  basic_usage.py
  enhanced_demo.py
```

## Développement

Installer une copie éditable et lancer la suite de tests :

```bash
pip install -e .
pytest
```

L'intégration continue lance `pytest` sur Python 3.8 à 3.11 pour les
pushes et pull requests vers `main`.

## Contribution

Les contributions sont bienvenues. Ouvrez une issue pour discuter d'un
changement avant de soumettre une pull request, couvrez tout nouveau
comportement par des tests et suivez le style de code existant.

## Remerciements

- [BEPb/image_to_ascii](https://github.com/BEPb/image_to_ascii) pour les
  idées d'entrée URL, de conversion vidéo et de galeries adoptées ici
- Paul Bourke pour les tables de densité canoniques
  ([Character representation of grey scale images](http://www.paulbourke.net/dataformats/asciiart/))
- Alex Harri Jónsson et le benchmark pixquill pour la littérature sur le
  rendu sensible aux formes, à l'origine de la surimpression de contours
  et de la table mesurée
- Lorem Picsum pour la photo de chiot de démonstration (id 237, licence Unsplash)

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE)
pour les détails.
