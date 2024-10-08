import sys
from cx_Freeze import setup, Executable

# Remplace 'app.py' par le nom de ton fichier principal
# Ajoute ici des fichiers supplémentaires que tu souhaites inclure
files = ['dummy_item_data.json']  # liste des fichiers à inclure s’il y en a

# Définir la configuration de setup
setup(
    name="AlmaPrintGrid",  # Nom de l'application
    version="0.1",         # Version
    description="Print documents callnumbers by scaning barcodes",  # Description
    options={"build_exe": {"include_files": files}},  # Inclusion des fichiers
    executables=[Executable("app.py")],  # Point d'entrée de ton application
)