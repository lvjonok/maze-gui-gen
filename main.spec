# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
            pathex=['/home/leo/Documents/projects/maze-gui-gen'],
            binaries=[],
            datas=[("source/app_screenshots/out_1.png", "source/app_screenshots/out_1.png"),
                    ("source/app_screenshots/out_2.png", "source/app_screenshots/out_2.png"), 
                    ("source/app_screenshots/out_3.png", "source/app_screenshots/out_3.png"), 
                    ("source/app_screenshots/out_4.png", "source/app_screenshots/out_4.png"), 
                    ("source/app_screenshots/out_5.png", "source/app_screenshots/out_5.png")
                    ],
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
          [("out_1.png", "source/app_screenshots/out_1.png", "source/app_screenshots/out_1.png"),
                    ("out_2.png", "source/app_screenshots/out_2.png", "source/app_screenshots/out_2.png"), 
                    ("out_3.png", "source/app_screenshots/out_3.png", "source/app_screenshots/out_3.png"), 
                    ("out_4.png", "source/app_screenshots/out_4.png", "source/app_screenshots/out_4.png"), 
                    ("out_5.png", "source/app_screenshots/out_5.png", "source/app_screenshots/out_5.png")],
          name='maze-gui-gen',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='maze.ico')
