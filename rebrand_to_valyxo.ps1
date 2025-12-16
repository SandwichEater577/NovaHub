# Read source file
$src = Get-Content -Path 'c:\Users\MichalStanistalKostk\Documents\NovaHub (Github)\NovaHub\src\Novahub.py' -Raw -Encoding UTF8

# Perform all replacements
$replacements = @{
    'NovaHubShell' = 'ValyxoShell'
    'NovaFileSystem' = 'ValyxoFileSystem'
    'NovaScriptRuntime' = 'ValyxoScriptRuntime'
    'NovaGPTModule' = 'ValyxoGPTModule'
    'NovaJobsManager' = 'ValyxoJobsManager'
    'NovaManSystem' = 'ValyxoManSystem'
    'highlight_novascript' = 'highlight_valyxoscript'
    'NovaScript' = 'ValyxoScript'
    'NovaGPT' = 'ValyxoGPT'
    'NovaHubDocuments' = 'ValyxoDocuments'
    'NovaHub' = 'Valyxo'
    'NScript' = 'VScript'
    'NGPT' = 'VGPT'
    'Valyxo D-Edition v1.1' = 'Valyxo v0.31'
}

foreach ($key in $replacements.Keys) {
    $src = $src.Replace($key, $replacements[$key])
}

# Write destination file
$dest = 'c:\Users\MichalStanistalKostk\Documents\NovaHub (Github)\NovaHub\src\Valyxo.py'
$src | Out-File -FilePath $dest -Encoding UTF8 -NoNewline

Write-Host "Created: $dest"
Write-Host "Size: $($src.Length) bytes"
