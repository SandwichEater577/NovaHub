$srcPath = 'c:\Users\MichalStanistalKostk\Documents\NovaHub (Github)\NovaHub\src\Novahub.py'
$dstPath = 'c:\Users\MichalStanistalKostk\Documents\NovaHub (Github)\NovaHub\src\Valyxo.py'

$content = [IO.File]::ReadAllText($srcPath, [System.Text.Encoding]::UTF8)

$reps = @{
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

foreach ($k in $reps.Keys) {
    $content = $content.Replace($k, $reps[$k])
}

[IO.File]::WriteAllText($dstPath, $content, [System.Text.Encoding]::UTF8)
Write-Output "OK: $dstPath"
