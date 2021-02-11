<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$ProcessName	
)
try{
	Stop-Process -Name $ProcessName -ErrorAction Stop
	Set-Content -Path 'C:\StoppedOutput.txt' -Value 'Process stopped'
}
catch [System.Management.Automation.ParameterBindingException]
{
    Write-Output "Parameters are not provided correctly"
}
catch [Microsoft.PowerShell.Commands.ProcessCommandException]
{
    Write-Output "Cannot find the process name"
}
catch 
{
    Write-Output "General Exception occured"
}


