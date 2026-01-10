<#
Sign an executable using a PFX file (signtool recommended).

Usage:
  .\sign_with_pfx.ps1 -PfxPath .\certs\pdfbinder_self.pfx -Password (ConvertTo-SecureString -String 'pass' -AsPlainText -Force) -FilePath .\dist_ps6\PdfBinder_PySide6.exe

If `signtool` is available (Windows SDK), it will be used. Otherwise the script will try `osslsigncode` if installed.
#>
param(
    [Parameter(Mandatory=$true)] [string]$PfxPath,
    [Parameter(Mandatory=$true)] [System.Security.SecureString]$Password,
    [Parameter(Mandatory=$true)] [string]$FilePath
)

if (-not (Test-Path $PfxPath)) { Write-Error "PFX not found: $PfxPath"; exit 1 }
if (-not (Test-Path $FilePath)) { Write-Error "File not found: $FilePath"; exit 1 }

$plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))

if (Get-Command signtool -ErrorAction SilentlyContinue) {
    Write-Output "Using signtool to sign $FilePath"
    signtool sign /f $PfxPath /p $plain /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 $FilePath
} elseif (Get-Command osslsigncode -ErrorAction SilentlyContinue) {
    Write-Output "Using osslsigncode to sign $FilePath (no timestamp)"
    osslsigncode sign -pkcs12 $PfxPath -pass $plain -n "PdfBinder" -in $FilePath -out ${FilePath}.signed
    Move-Item -Force ${FilePath}.signed $FilePath
} else {
    Write-Warning "No signing tool found. Install Windows SDK (signtool) or osslsigncode."
    exit 1
}

Write-Output "Signing complete. Verify with: Get-AuthenticodeSignature $FilePath"
