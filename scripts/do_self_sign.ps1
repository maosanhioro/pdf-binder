$certDir = ".\certs"
New-Item -ItemType Directory -Force -Path $certDir | Out-Null

# generate random password
$bytes = New-Object byte[] 16
[System.Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($bytes)
$pwd = [Convert]::ToBase64String($bytes)
$sec = ConvertTo-SecureString -String $pwd -AsPlainText -Force

Write-Output "Generated PFX password (base64): $pwd"

Write-Output "Creating self-signed PFX..."
try {
    & .\scripts\create_self_pfx.ps1 -Subject 'CN=PdfBinder Self-Sign' -OutPfx ".\certs\pdfbinder_self.pfx" -Password $sec
}
catch {
    Write-Error "create_self_pfx threw an exception: $_"
    exit 1
}

if (-not (Test-Path -Path ".\certs\pdfbinder_self.pfx")) {
    Write-Error "create_self_pfx did not produce PFX: .\certs\pdfbinder_self.pfx"
    exit 1
}

Write-Output "Looking up certificate in CurrentUser\My store..."
$cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object { $_.Subject -like '*PdfBinder Self-Sign*' } | Select-Object -First 1
if ($null -eq $cert) {
    Write-Error "Certificate not found in store"
    exit 1
}

Write-Output "Signing dist_ps6\\PdfBinder_PySide6.exe with Set-AuthenticodeSignature (no timestamp)..."
try {
    $sig = Set-AuthenticodeSignature -FilePath ".\dist_ps6\PdfBinder_PySide6.exe" -Certificate $cert -HashAlgorithm 'SHA256' -ErrorAction Stop
}
catch {
    Write-Error "Set-AuthenticodeSignature failed: $_"
    exit 1
}

$sig | Format-List

Write-Output "Verification result:"
$verify = Get-AuthenticodeSignature ".\dist_ps6\PdfBinder_PySide6.exe"
$verify | Format-List

if ($verify.Status -ne 'Valid') {
    Write-Error "Signature verification failed or is not valid: $($verify.Status)"
    exit 1
}

Write-Output "Done. Keep the PFX at: .\certs\pdfbinder_self.pfx and password shown above for future use."
exit 0
