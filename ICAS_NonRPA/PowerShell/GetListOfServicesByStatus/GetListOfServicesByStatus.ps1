<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$Status,
	[String]$OutFilePath	
)
Get-Service | Where-Object {$_.Status -EQ $Status} | Out-File $OutFilePath 