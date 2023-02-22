# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

py_files = [
    'bin/GGdog_game.py'
]

add_files = [
    ('tttf/font.ttf', 'tttf'),
    ('images/background.png', 'images'),
    ('images/barrier_icon.png', 'images'),
    ('images/barrier.png', 'images'),
    ('images/bullet.png', 'images'),
    ('images/expl1.png', 'images'),
    ('images/expl2.png', 'images'),
    ('images/expl0.png', 'images'),
    ('images/expl3.png', 'images'),
    ('images/expl4.png', 'images'),
    ('images/expl5.png', 'images'),
    ('images/expl6.png', 'images'),
    ('images/expl7.png', 'images'),
    ('images/expl8.png', 'images'),
    ('images/gun.png', 'images'),
    ('images/missile.png', 'images'),
    ('images/player_expl0.png', 'images'),
    ('images/player_expl1.png', 'images'),
    ('images/player_expl2.png', 'images'),
    ('images/player_expl4.png', 'images'),
    ('images/player_expl3.png', 'images'),
    ('images/player_expl5.png', 'images'),
    ('images/player_expl6.png', 'images'),
    ('images/player_expl7.png', 'images'),
    ('images/player_expl8.png', 'images'),
    ('images/rock0.png', 'images'),
    ('images/rock1.png', 'images'),
    ('images/rock2.png', 'images'),
    ('images/rock3.png', 'images'),
    ('images/rock4.png', 'images'),
    ('images/rock5.png', 'images'),
    ('images/rock6.png', 'images'),
    ('images/shield.png', 'images'),
    ('images/tato.ico', 'images'),
    ('images/player.ico', 'images'),
  

    ('sound/background.wav', 'sound'),
    ('sound/barrier_break.wav', 'sound'),
    ('sound/barrier_on.wav', 'sound'),
    ('sound/expl0.wav', 'sound'),
    ('sound/expl1.wav', 'sound'),
    ('sound/get_hurt.wav', 'sound'),
    ('sound/pow0.wav', 'sound'),
    ('sound/pow0.wav', 'sound'),
    ('sound/rumble.wav', 'sound'),
    ('sound/shoot.wav', 'sound'),
    ('sound/BATTLE.mp3', 'sound'),
    ]


a = Analysis(py_files,
             pathex=['/Users/infinity5050/Desktop/P5050'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GGdog_game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='/Users/infinity5050/Desktop/P5050/images/player.ico' )