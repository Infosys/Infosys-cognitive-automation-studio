<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$FilePath	
)
try{
	Get-ExecutionPolicy -List | Out-File $FilePath -ErrorAction Stop
}
catch [System.IO.DirectoryNotFoundException]
{
    Write-Output "The directory was not found: [$FilePath]"
}
catch 
{
    Write-Output "General Exception occured"
}
