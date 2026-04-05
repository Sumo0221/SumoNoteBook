# Sumo Learning Sync Script

$ErrorActionPreference = "SilentlyContinue"

$SOURCE_BASE = "C:\Users\rayray\.openclaw"
$DEST_BASE = "C:\butler_sumo\library\SumoNoteBook\learning"

# Sync lawyer
Write-Host "Syncing lawyer learning..."
$dest = "$DEST_BASE\lawyer"
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
$sourceFiles = @(
    "$SOURCE_BASE\workspace\memory\law_study",
    "$SOURCE_BASE\workspace\memory\law_study_afternoon_runs.md",
    "$SOURCE_BASE\workspace\memory\law_study_append.md",
    "$SOURCE_BASE\workspace\memory\law_study_car_accident.md"
)
$count = 0
foreach ($f in $sourceFiles) {
    if (Test-Path $f) {
        $name = Split-Path $f -Leaf
        Copy-Item $f -Destination "$dest\$name" -Force
        $count++
    }
}
Write-Host "  Done: $count files"

# Sync fengshui
Write-Host "Syncing fengshui learning..."
$dest = "$DEST_BASE\fengshui"
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
$sourceFiles = @(
    "$SOURCE_BASE\workspace_fengshui\memory\mysticism_study.md"
)
$count = 0
foreach ($f in $sourceFiles) {
    if (Test-Path $f) {
        $name = Split-Path $f -Leaf
        Copy-Item $f -Destination "$dest\$name" -Force
        $count++
    }
}
Write-Host "  Done: $count files"

# Sync engineer
Write-Host "Syncing engineer learning..."
$dest = "$DEST_BASE\engineer"
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
$sourceFiles = @(
    "$SOURCE_BASE\workspace_engineer\memory\engineer_cs_study.md",
    "$SOURCE_BASE\workspace_engineer\memory\engineer_tdd_study.md",
    "$SOURCE_BASE\workspace_engineer\memory\engineer_tool_filter.md",
    "$SOURCE_BASE\workspace_engineer\memory\glm_ocr_poc.md"
)
$count = 0
foreach ($f in $sourceFiles) {
    if (Test-Path $f) {
        $name = Split-Path $f -Leaf
        Copy-Item $f -Destination "$dest\$name" -Force
        $count++
    }
}
Write-Host "  Done: $count files"

Write-Host "All done!"
