/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.excel;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name="WriteExcel",version="1.0",description="",botCategory="String",author="", technology = "Java",
technologyCode="01",botCategoryCode="03",botId="04") 
public class WriteExcel {
	private static final Logger log = LoggerFactory.getLogger(WriteExcel.class);
	@Errors(exceptions= {
			@Error(errorCode = "01030411FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0103041115", errorMessagePattern = "Table Does Not Exist", exceptionClass = IOException.class),
			@Error(errorCode="0103041101", errorMessagePattern ="Folder Path Does Not Exist" , exceptionClass=IOException.class)
		})
	
	public Status execute(
			@InputParameter(name="SourceData") Map<String, String> sourceData,
			@InputParameter(name="FolderPath",constraints= { EXISTS, FOLDER}) String folderPath,
			@InputParameter(name="SheetName") String sheetName,
			@InputParameter(name="FileName") String fileName,
			@OutputParameter(name="ReportFilePath") ObjectHolder <String> reportFilePath
			
			) throws ExecutionError, IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA = "1";
		String errorCodeB;
		String errorDescrption;
		
		if(sourceData.values().isEmpty())
		{
			errorCategoryCode = "1";
			errorCodeB = "15";
			errorDescrption = "Table Does Not Exist";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + sourceData);
		}
		
		try {
			System.out.println("SourceData"+sourceData);
			reportFilePath.setValue(CreateNewExcel(sourceData,sheetName,folderPath,fileName));
			
			return new Status("00","Creation of Excel is Done ");
		} catch (Exception e) {
			
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}

	
	}
	
		
		public static  String CreateNewExcel(Map<String, String> sourceData,String sheetName,String filePath,String fileName){

        XSSFWorkbook wb = new XSSFWorkbook(); 
        
        //Create a blank sheet
        
        XSSFSheet sheet = wb.createSheet(sheetName);

		//HashMap<String, String> data = new HashMap<>();

//		data.put("EmployeeNumber", "123");
//		data.put("EmployeeName", "Ashish");
//		data.put("Unit", "GDLY");
//		data.put("Salary", "11340.20");
//		data.put("Validation", "Failed([Salary, Unit])");
		
		 Set<Map.Entry<String,String>> pair = sourceData.entrySet(); 
		 
		 Row row=sheet.createRow(0);
		 int cellpointer=0;
		 
		 for (Entry<String, String> map : pair) {
			 
			 Cell cell=row.createCell(cellpointer++);
			 //System.out.println("Test=== " + map.getKey());
			 cell.setCellValue(map.getKey());
			 
		 }
		 cellpointer=0;
		 row=sheet.createRow(1);
		 for (Entry<String, String> map : pair) {
			 
			 Cell cell=row.createCell(cellpointer++);
			 
			 System.out.println("Test=== " + map.getValue());
			 cell.setCellValue(map.getValue());
			 
		 }
		 String output="";
		 try
	        {
	            //Write the workbook in file system
			 	File outputfile=new File(filePath+File.separator+fileName);
	            FileOutputStream out = new FileOutputStream(outputfile);
	            wb.write(out);
	            out.close();
	            System.out.println(" written successfully on disk.");
	            output=filePath+File.separator+fileName;
	            
	            
	        } 
	        catch (Exception e) 
	        {
	            e.printStackTrace();
	        }
		return output;
		 
				
		
		 
	}	
}
