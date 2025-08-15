$problem = "2131E"

Write-Host "compiling:"
g++ -std=c++17 "$problem.cpp" -o $problem
Write-Host "compilation done!"
Write-Host "running:"

$start = Get-Date
& .\"$problem" < "$problem.input" > "$problem.output"
$ret_code = $LASTEXITCODE

$elapsed = (Get-Date) - $start
Write-Host "executed in $($elapsed.Seconds)s"
Write-Host "terminated returning $ret_code"