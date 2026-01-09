<#
Create a self-signed code signing certificate (PFX) for local testing.
This is NOT trusted by Microsoft SmartScreen, but can be used to sign locally.

Usage:
  .\create_self_pfx.ps1 -Subject "CN=PdfBinder Test" -OutPfx .\certs\pdfbinder_test.pfx -Password (ConvertTo-SecureString -String 'pass' -AsPlainText -Force)

The script creates a code-signing certificate in the CurrentUser\My store and exports a PFX.
#>
<#
Create a self-signed code signing certificate (PFX) for local testing.
This is NOT trusted by Microsoft SmartScreen, but can be used to sign locally.

Usage:
  .\create_self_pfx.ps1 -Subject "CN=PdfBinder Test" -OutPfx .\certs\pdfbinder_test.pfx -Password (ConvertTo-SecureString -String 'pass' -AsPlainText -Force)

The script creates a code-signing certificate in the CurrentUser\My store and exports a PFX.
#>
param(
    [string]$Subject = "CN=PdfBinder Self-Sign",
    [string]$OutPfx = ".\certs\pdfbinder_self.pfx",
    [System.Security.SecureString]$Password
)

if (-not $Password) {
    Write-Error "Password (SecureString) is required to export PFX. Construct with ConvertTo-SecureString."
    exit 1
}

try {
    New-Item -Path (Split-Path $OutPfx) -ItemType Directory -Force | Out-Null

    $cert = New-SelfSignedCertificate -Subject $Subject -Type CodeSigningCert -KeyExportPolicy Exportable -KeySpec Signature -NotAfter (Get-Date).AddYears(1) -CertStoreLocation Cert:\CurrentUser\My -ErrorAction Stop

    if (-not $cert) {
        throw "Failed to create certificate"
    }

    Export-PfxCertificate -Cert $cert -FilePath $OutPfx -Password $Password -ErrorAction Stop

    if (-not (Test-Path -Path $OutPfx)) {
        throw "PFX export failed: $OutPfx not found after export"
    }

    Write-Output "PFX exported to: $OutPfx"
    exit 0
}
catch {
    Write-Error "create_self_pfx error: $_"
    exit 1
}