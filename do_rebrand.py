import os

src_path = r'src\Novahub.py'
output_path = r'src\Valyxo.py'

with open(src_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('NovaHubShell', 'ValyxoShell'),
    ('NovaHubDocuments', 'ValyxoDocuments'),
    ('NovaFileSystem', 'ValyxoFileSystem'),
    ('NovaScriptRuntime', 'ValyxoScriptRuntime'),
    ('NovaGPTModule', 'ValyxoGPTModule'),
    ('NovaJobsManager', 'ValyxoJobsManager'),
    ('NovaManSystem', 'ValyxoManSystem'),
    ('highlight_novascript', 'highlight_valyxoscript'),
    ('NovaScript', 'ValyxoScript'),
    ('NovaGPT', 'ValyxoGPT'),
    ('nova_logo', 'valyxo_logo'),
    ('NovaHub', 'Valyxo'),
    ('NScript', 'VScript'),
    ('NGPT', 'VGPT'),
    ('Valyxo D-Edition v1.1', 'Valyxo v0.31'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: Valyxo.py created")
