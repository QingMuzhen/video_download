# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有需要的数据文件
datas = [
    ('config.ini', '.'),
    ('README.md', '.'),
]

# 收集隐藏导入
hiddenimports = [
    'selenium',
    'selenium.webdriver',
    'selenium.webdriver.chrome.service',
    'selenium.webdriver.chrome.options',
    'selenium.webdriver.common.by',
    'selenium.webdriver.support.ui',
    'selenium.webdriver.support.expected_conditions',
    'selenium.common.exceptions',
    'bs4',
    'requests',
    'tqdm',
    'urllib3',
    'certifi',
    'charset_normalizer',
    'idna',
    'packaging',
    'packaging.version',
    'tkinter',
    'tkinter.ttk',
    'tkinter.scrolledtext',
    'tkinter.messagebox',
    'tkinter.filedialog',
]

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# pyi_splash = Splash(
#     'splash.png',
#     binaries=a.binaries,
#     datas=a.datas,
#     text_pos=(10, 50),
#     text_size=12,
#     text_color='white',
#     minify_script=True,
#     always_on_top=True,
# )

pyi_splash = None  # 没有splash.png，已注释掉Splash部分

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    # splash,  # 如果使用splash，取消注释
    # splash.binaries,  # 如果使用splash，取消注释
    [],
    name='视频爬虫工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # 如果有图标文件，取消注释
)
