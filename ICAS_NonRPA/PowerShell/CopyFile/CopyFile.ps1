<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$Path,
	[String]$Destination	
)

echo Path $Path

Copy-Item -Path $Path -Destination $Destination