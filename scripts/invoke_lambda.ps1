param(
  [Parameter(Mandatory = $true)]
  [string]$FunctionName,

  [string]$OutFile = "response.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
  throw "AWS CLI not found on PATH. Verify with 'aws --version'."
}

$resolvedOutFile = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutFile)
$outDir = Split-Path -Parent $resolvedOutFile
if ($outDir -and -not (Test-Path $outDir)) {
  New-Item -ItemType Directory -Path $outDir | Out-Null
}

$args = @(
  "lambda", "invoke",
  "--function-name", $FunctionName,
  "--cli-binary-format", "raw-in-base64-out",
  "--payload", "{}",
  $resolvedOutFile
)

& aws @args | Out-Host
if ($LASTEXITCODE -ne 0) {
  throw "aws lambda invoke failed with exit code $LASTEXITCODE"
}

if (-not (Test-Path $resolvedOutFile)) {
  throw "Expected output file was not created: $resolvedOutFile"
}

Get-Content $resolvedOutFile