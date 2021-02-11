<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$LogName,
	[String]$OutFilePath	
)
try{
	Get-EventLog -Log $LogName | Out-File $OutFilePath -ErrorAction SilentlyContinue
}
catch [System.InvalidOperationException]
{
    Write-Output "The event log of [$LogName] does not exist"
}
catch 
{
    Write-Output "General Exception occured"
}
