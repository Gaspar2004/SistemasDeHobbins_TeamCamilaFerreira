# Abre cada nodo pasado como argumento en su propia ventana de PowerShell.
# Uso (ejemplos):
#   powershell -ExecutionPolicy Bypass -File scripts\run_nodes.ps1 SGW PGW PCRF HSS
#   powershell -ExecutionPolicy Bypass -File scripts\run_nodes.ps1 UE1 UE2 eNB MME
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Nodes)

$map = @{
  "UE1" = "nodes\volte_ue_1\volte_ue_1.py"; "UE2" = "nodes\volte_ue_2\volte_ue_2.py";
  "eNB" = "nodes\enb\enb.py"; "MME" = "nodes\mme\mme.py";
  "SGW" = "nodes\sgw\sgw.py"; "PGW" = "nodes\pgw\pgw.py";
  "PCRF" = "nodes\pcrf\pcrf.py"; "HSS" = "nodes\hss\hss.py";
  "P-CSCF" = "nodes\pcscf\pcscf.py"; "I-CSCF" = "nodes\icscf\icscf.py";
  "S-CSCF" = "nodes\scscf\scscf.py"; "TAS" = "nodes\tas\tas.py"
}
$root = Split-Path -Parent $PSScriptRoot
foreach ($n in $Nodes) {
  $rel = $map[$n]
  if (-not $rel) { Write-Warning "Nodo desconocido: $n"; continue }
  $cmd = "Set-Location '$root'; python '$rel'"
  Start-Process powershell -ArgumentList @("-NoExit", "-Command", $cmd)
}
