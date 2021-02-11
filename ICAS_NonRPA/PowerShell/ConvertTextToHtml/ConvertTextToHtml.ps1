<#
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
#>
Param
(
	[String]$SourceFile ,
	[String]$TargetFile	
)
Try{
	$File = Get-Content $SourceFile -ErrorAction Stop
	$FileLine = @()
	Foreach ($Line in $File) {
	 $MyObject = New-Object -TypeName PSObject
	 Add-Member -InputObject $MyObject -Type NoteProperty -Name Test -Value $Line
	 $FileLine += $MyObject
	}
	$FileLine | ConvertTo-Html -Property Test | Out-File $TargetFile
}
catch [System.Management.Automation.ParameterBindingException]
{
    Write-Output "Parameters are not provided correctly"
}
catch [System.Management.Automation.ItemNotFoundException]
{
    Write-Output "Cannot find the privided file "
}
catch 
{
    Write-Output "General Exception occured"
}
