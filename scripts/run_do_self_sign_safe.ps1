# Stop any running PdfBinder processes (if present) and run do_self_sign.ps1 safely
$procs = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'PdfBinder' -or $_.ProcessName -match 'pdfbinder' -or ($_.MainWindowTitle -and $_.MainWindowTitle -match 'PdfBinder') }
if ($procs) {
    Write-Output 'Stopping processes:'
    $procs | Select-Object Id, ProcessName, MainWindowTitle | Format-Table -AutoSize
    $procs | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 500
}
else {
    Write-Output 'No PdfBinder processes found.'
}

Write-Output 'Running do_self_sign.ps1...'
$scriptPath = Join-Path -Path $PSScriptRoot -ChildPath 'do_self_sign.ps1'
if (-not (Test-Path $scriptPath)) {
    Write-Error "do_self_sign.ps1 not found at: $scriptPath"
    exit 1
}
powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath
exit $LASTEXITCODE
exit $LASTEXITCODE
