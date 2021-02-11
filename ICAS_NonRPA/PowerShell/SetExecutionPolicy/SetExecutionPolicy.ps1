<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$ExecutionPolicy,
	[String]$Scope	
)
try{

	Set-ExecutionPolicy -ExecutionPolicy $ExecutionPolicy -Scope $Scope -ErrorAction Stop
	"Success"
}
catch [System.Management.Automation.ParameterBindingException]
{
    Write-Output "Parameters are not provided correctly"
}
catch [System.UnauthorizedAccessException]
{
    Write-Output "Unauthorized access"
}
catch 
{
    Write-Output "General Exception occured"
}


