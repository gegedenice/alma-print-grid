# app.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Analyse le script principal de l'application
a = Analysis(['app.py'],
             pathex=[],
             binaries=[],
             datas=[('dummy_item_data.json', '.')],  # Assurez-vous d'ajouter toutes les données nécessaires
             hiddenimports=['pyexpat', 'pkg_resources.py2_warn'],  # Assurez-vous d'ajouter toutes les importations cachées nécessaires
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             noarchive=False,
             optimize=0,
             cipher=block_cipher)

# Crée l'archive PYZ à partir des scripts Python
pyz = PYZ(a.pure, cipher=block_cipher)  # Supprimé a.zipped

# Crée l'exécutable
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='app',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,  # Garde la console pour le débogage
          disable_windowed_traceback=False,
          argv_emulation=False)

# Collecte des fichiers binaires et de données
coll = COLLECT(exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                upx_exclude=[],
                name='app')

