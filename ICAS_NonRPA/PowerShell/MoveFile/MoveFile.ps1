<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$SourceFile,
	[String]$TargetLocation	
)
try{
	Move-Item -Path $SourceFile -Destination $TargetLocation -ErrorAction Stop
}
catch [System.Management.Automation.ItemNotFoundException]
{
    Write-Output "The path or file was not found: [$SourceFile]"
}
catch 
{
    Write-Output "General Exception occured"
}
