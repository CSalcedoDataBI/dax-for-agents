<#
.SYNOPSIS
    Rebuilds the dax-lib INDEX of the DAX Lib registry (https://daxlib.org).

.DESCRIPTION
    daxlib.org is a JavaScript SPA and cannot be scraped with a plain HTTP GET.
    The source of truth is the GitHub repo, where every package version lives at
        packages/{letter}/{id}/{version}/{manifest.daxlib, lib/functions.tmdl}
    This script shallow-clones that repo, reads each manifest, parses the function
    names out of its TMDL, and writes catalog.json + catalog.md stamped with the
    upstream commit.

    It KEEPS NO .tmdl FILE. This repository indexes the registry; it does not
    redistribute other people's DAX code. See docs/decisions/2026-08-10-dax-lib-
    catalog-only.md, and dax-lib/NOTICE for the attribution that does apply.

    Re-runnable: it rewrites the catalog files from scratch.

.PARAMETER SkillRoot
    Root of the dax-lib skill. Defaults to the parent of this script's folder.

.PARAMETER TempDir
    Where to shallow-clone the repo. Defaults to a temp sibling, removed on exit.

.EXAMPLE
    pwsh ./scripts/refresh-daxlib.ps1
#>
[CmdletBinding()]
param(
    [string]$SkillRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$TempDir   = (Join-Path ([System.IO.Path]::GetTempPath()) "daxlib-extract"),
    [string]$RepoUrl   = "https://github.com/daxlib/daxlib.git"
)

$ErrorActionPreference = "Stop"
$catalogJson = Join-Path $SkillRoot "catalog.json"
$catalogMd   = Join-Path $SkillRoot "catalog.md"

Write-Host "DAX Lib extraction -> $SkillRoot"

# 1. Fresh shallow clone -------------------------------------------------------
if (Test-Path $TempDir) { Remove-Item -Recurse -Force $TempDir }
Write-Host "Cloning $RepoUrl (depth 1)..."
git clone --depth 1 $RepoUrl $TempDir 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { throw "git clone failed ($LASTEXITCODE)" }

$repoSha = (git -C $TempDir rev-parse --short HEAD).Trim()
$repoDate = (git -C $TempDir log -1 --format=%cI).Trim()

# 2. Collect manifests ---------------------------------------------------------
$manifests = Get-ChildItem -Path (Join-Path $TempDir "packages") -Recurse -Filter "manifest.daxlib"
Write-Host "Found $($manifests.Count) package versions."

$packages = foreach ($m in $manifests) {
    $verDir   = $m.Directory                                   # .../{id}/{version}
    $tmdlSrc  = Join-Path $verDir.FullName "lib/functions.tmdl"
    if (-not (Test-Path $tmdlSrc)) { Write-Warning "no functions.tmdl for $($m.FullName)"; continue }

    $meta = Get-Content -Raw $m.FullName | ConvertFrom-Json
    $id      = $meta.id
    $version = "$($meta.version)"

    # Deliberately NOT copied: the .tmdl and the manifest stay in the clone, which is
    # discarded. Only the metadata below is kept. Restoring a copy here would turn this
    # repo back into a redistributor of 40 other authors' work.

    # parse function names out of the clone: lines like  function 'Name' = ...
    $fns = Select-String -Path $tmdlSrc -Pattern "^\s*function\s+'([^']+)'" -AllMatches |
           ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

    $tags = @()
    if ($meta.tags) { $tags = ($meta.tags -split ',') | ForEach-Object { $_.Trim() } | Where-Object { $_ } }

    [pscustomobject]@{
        id          = $id
        version     = $version
        authors     = "$($meta.authors)"
        description = "$($meta.description)"
        tags        = $tags
        functions   = @($fns)
        url         = "https://github.com/daxlib/daxlib/tree/main/packages/$($id.Substring(0,1).ToLower())/$($id.ToLower())"
    }
}

# 3. Mark latest version per id (best-effort semver, non-prerelease wins) ------
function ConvertTo-SortableVersion([string]$v) {
    $base = ($v -split '-')[0]
    $pre  = $v.Contains('-')
    try { $ver = [version]$base } catch { $ver = [version]"0.0.0.0" }
    [pscustomobject]@{ Ver = $ver; IsPre = $pre; Raw = $v }
}
$byId = $packages | Group-Object id
foreach ($g in $byId) {
    $latest = $g.Group | Sort-Object `
        @{ Expression = { (ConvertTo-SortableVersion $_.version).Ver } }, `
        @{ Expression = { -not (ConvertTo-SortableVersion $_.version).IsPre } } |
        Select-Object -Last 1
    foreach ($p in $g.Group) {
        $p | Add-Member -NotePropertyName isLatest -NotePropertyValue ($p.version -eq $latest.version) -Force
    }
}

$packages = $packages | Sort-Object id, version

# 4. catalog.json -------------------------------------------------------------
$catalog = [ordered]@{
    source              = "daxlib/daxlib@$repoSha"
    sourceCommitDate    = $repoDate
    packageVersionCount = $packages.Count
    packageCount        = $byId.Count
    functionCount       = [int](($packages | ForEach-Object { $_.functions.Count } | Measure-Object -Sum).Sum)
    packages            = $packages
}
$catalog | ConvertTo-Json -Depth 6 | Set-Content -Path $catalogJson -Encoding UTF8
Write-Host "Wrote catalog.json ($($byId.Count) packages, $($packages.Count) versions)."

# 5. catalog.md (human index, latest version per package, grouped by tag) -----
$latestOnly = $packages | Where-Object isLatest | Sort-Object id
$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine("# DAX Lib — Catálogo de paquetes (índice generado)")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("> Fuente: ``daxlib/daxlib@$repoSha`` · commit $repoDate")
[void]$sb.AppendLine("> $($byId.Count) paquetes · $($packages.Count) versiones · $($catalog.functionCount) funciones")
[void]$sb.AppendLine("> Regenerar: ``pwsh ./scripts/refresh-daxlib.ps1``.")
[void]$sb.AppendLine("> **Indice solamente** - el codigo DAX no se redistribuye aqui. Instala desde [daxlib.org](https://daxlib.org) o Tabular Editor 3 (DAX Package Manager).")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Paquete | Última | Autor | Funciones | Descripción |")
[void]$sb.AppendLine("|---|---|---|---|---|")
foreach ($p in $latestOnly) {
    $fnList = if ($p.functions.Count -le 4) { ($p.functions -join ', ') } else { "$($p.functions.Count) fns" }
    $desc = $p.description -replace '\|','\|' -replace '\r?\n',' '
    [void]$sb.AppendLine("| ``$($p.id)`` | $($p.version) | $($p.authors) | $fnList | $desc |")
}
$sb.ToString() | Set-Content -Path $catalogMd -Encoding UTF8
Write-Host "Wrote catalog.md."

# 6. Cleanup ------------------------------------------------------------------
Remove-Item -Recurse -Force $TempDir
Write-Host "Done. Temp clone removed."
