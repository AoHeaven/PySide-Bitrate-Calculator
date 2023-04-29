# Путь к файлу bitrate_calculator.pyw
$filePath = ".\bitrate_calculator.pyw"

# Активация виртуального окружения
$venvPath = ".\.venv"
$activateScript = Join-Path $venvPath "\Scripts\activate.ps1"
& $activateScript

# Запуск файла bitrate_calculator.pyw
& $filePath

