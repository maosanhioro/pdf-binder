<#
Create a SHA256 checksum file for the EXE (detached signature-like artifact).
This does not replace Authenticode signing but is useful to verify integrity.

Usage:
  .\sign_detached.ps1 -FilePath .\dist\PdfBinder.exe -OutFile .\dist\PdfBinder.exe.sha256
#>
param(
    [string]$FilePath = ".\dist\PdfBinder.exe",
    [string]$OutFile = ".\dist\PdfBinder.exe.sha256"
)

if (-not (Test-Path $FilePath)) { Write-Error "File not found: $FilePath"; exit 1 }

$hash = Get-FileHash -Algorithm SHA256 -Path $FilePath
$hash.Hash | Out-File -FilePath $OutFile -Encoding ASCII

Write-Output "SHA256 checksum written to: $OutFile"