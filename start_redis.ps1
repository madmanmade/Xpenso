# Get the current directory where the script is located
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$redisPath = Join-Path -Path $scriptPath -ChildPath "Redis\Redis-7.4.3-Windows-x64-msys2"
$redisServer = Join-Path -Path $redisPath -ChildPath "redis-server.exe"
$redisCli = Join-Path -Path $redisPath -ChildPath "redis-cli.exe"

Write-Host "Starting Redis Server..."
Write-Host "Using Redis at: $redisServer"

try {
    # Try to ping Redis first to see if it's already running
    $pingResult = & $redisCli ping 2>&1
    if ($LASTEXITCODE -eq 0 -and $pingResult -eq "PONG") {
        Write-Host "Redis is already running!" -ForegroundColor Green
    }
    else {
        # Start Redis server with configuration
        $configPath = Join-Path -Path $redisPath -ChildPath "redis.conf"
        $process = Start-Process -FilePath $redisServer -ArgumentList $configPath -NoNewWindow -PassThru
        
        # Wait a moment for Redis to start
        Start-Sleep -Seconds 2
        
        # Verify Redis is running
        $pingResult = & $redisCli ping 2>&1
        if ($LASTEXITCODE -eq 0 -and $pingResult -eq "PONG") {
            Write-Host "Redis server started successfully!" -ForegroundColor Green
            Write-Host "Redis is running on localhost:6379" -ForegroundColor Cyan
        }
        else {
            Write-Host "Failed to verify Redis connection" -ForegroundColor Red
            Write-Host "Error: $pingResult" -ForegroundColor Red
        }
    }
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`nPress Enter to exit..." -ForegroundColor Yellow
$null = Read-Host 