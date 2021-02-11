$path = $args[0]
$xlFixedFormat = "Microsoft.Office.Interop.Excel.xlFixedFormatType" -as [type] 
$excelFiles = Get-ChildItem -Path $path -include *.xlsx -recurse 
$objExcel = New-Object -ComObject excel.application 
$objExcel.visible = $false 
foreach($wb in $excelFiles) 
{ 
 $filepath = ($wb.FullName -replace '.xlsx?$', '.pdf')
 $workbook = $objExcel.workbooks.open($wb.fullname, 3) 
 $workbook.Saved = $true 
"saving $filepath"
 $workbook.ExportAsFixedFormat($xlFixedFormat::xlTypePDF, $filepath) 
 $objExcel.Workbooks.close() 
} 
$objExcel.Quit()