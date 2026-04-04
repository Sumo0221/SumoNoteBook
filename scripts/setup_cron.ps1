# SumoNoteBook Cron Setup Script
# Run as Administrator

$scripts = @{
    "SumoNoteBook_DailyOrganizer" = @{
        Path = "c:\butler_sumo\library\SumoNoteBook\scripts\daily_organizer.py"
        Time = "04:12"
        Desc = "SumoNoteBook Daily Organization"
    }
    "SumoNoteBook_HealthCheck" = @{
        Path = "c:\butler_sumo\library\SumoNoteBook\scripts\health_check.py"
        Time = "05:21"
        Desc = "SumoNoteBook Health Check"
    }
}

Write-Host "SumoNoteBook Cron Setup"
Write-Host "======================="

foreach ($name in $scripts.Keys) {
    $task = $scripts[$name]
    
    $existing = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    
    if ($existing) {
        Write-Host "[skip] $name already exists"
        continue
    }
    
    $trigger = New-ScheduledTaskTrigger -Daily -At $task.Time
    $action = New-ScheduledTaskAction -Execute "python" -Argument $task.Path
    Register-ScheduledTask -TaskName $name -Trigger $trigger -Action $action -Description $task.Desc -RunLevel Highest
    
    Write-Host "[OK] $name scheduled (daily at $($task.Time))"
}

Write-Host ""
Write-Host "Done! Check tasks with:"
Write-Host "  Get-ScheduledTask -TaskName 'SumoNoteBook*'"
