<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$CommandName,
	[String]$OutFilePath	
)
try{
	$CommandName | ConvertTo-HTML | Out-File $OutFilePath -ErrorAction Stop
}
Catch [System.Management.Automation.CommandNotFoundException] {
    Write-Host 'Command not found ' 
}
Catch [System.IO.DirectoryNotFoundException] {
    Write-Host 'Directory not found ' 
}
Catch {
    "General exception occured "
}