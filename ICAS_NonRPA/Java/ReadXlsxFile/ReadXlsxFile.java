/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.excel;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.custom.table.Table;

@Bot(name = "ReadXlsxFile", version = "1.0", description = "", botCategory = "String", author = "",
technology = "", technologyCode = "01", botCategoryCode = "03", botId = "01")

//ErrorCategory(ValidationError: 1, ConnectionError: 2,AccessError : 3, DiskIOError: 4, DBIOError: 5,
//           NetworkIOError: 6, ConfigurationError: 7)
//botCode = technologyCode + categoryCode + botId
//botErrorCode = errorCategoryCode + errorCodeA + errorCodeB
//errorCode = botCode + botErrorCode 
//
//String botErrorCode;
//String errorCategoryCode;
//String errorCodeA = "1";
//String errorCodeB;
//String errorDescrption;

public class ReadXlsxFile {
	private static final Logger log = LoggerFactory.getLogger(ReadXlsxFile.class);
	@Errors(exceptions= {
			@Error(errorCode = "01030111FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0103011106", errorMessagePattern = " Is Not File ", exceptionClass = IOException.class),
			@Error(errorCode = "0103011103", errorMessagePattern = "File Does Not Exist", exceptionClass = IOException.class)
			})

	public Status execute(
			@InputParameter(name="SourceFile", constraints= {EXISTS, FILE, }) String fileName,
			@InputParameter(name="Hasheader") String hasHeader,
			@OutputParameter(name="Data") ObjectHolder<Table> table
			) throws Exception {

			log.info("*********************ReadXlsxFile**************************");			
			log.info("*********************SourceFile**************************"+fileName);
			
			FileInputStream excelFile = null;
        try {

        	excelFile = new FileInputStream(fileName);
            Workbook workbook = new XSSFWorkbook(excelFile);
            Sheet datatypeSheet = workbook.getSheetAt(0);
            List<com.infosys.impact.botfactory.custom.table.Row> rows = new ArrayList<com.infosys.impact.botfactory.custom.table.Row>();
            Iterator<Row> iterator = datatypeSheet.iterator();
 //           Table table = new Table();
            List<Object> list = null;
            com.infosys.impact.botfactory.custom.table.Row row = null;
            com.infosys.impact.botfactory.custom.table.Row header = new com.infosys.impact.botfactory.custom.table.Row();
            while (iterator.hasNext()) {
                Row currentRow = iterator.next();
                list = new ArrayList<Object>();
                Iterator<Cell> cellIterator = currentRow.iterator();
                row = new com.infosys.impact.botfactory.custom.table.Row();
                
				while (cellIterator.hasNext()) {
					Cell currentCell = cellIterator.next();
					if (currentCell.getCellTypeEnum() == CellType.STRING) {
						list.add(currentCell.getStringCellValue());
					} else if (currentCell.getCellTypeEnum() == CellType.NUMERIC) {
						list.add(currentCell.getNumericCellValue() + "");
					}
				}
				if (hasHeader.equalsIgnoreCase("true") && currentRow.getRowNum() == 0) {
					header.setCells(list);
				}else {
					row.setCells(list);
					rows.add(row);
				}
            }
//            Table table = new Table();
            Table T =  new Table();
            if (hasHeader.equalsIgnoreCase("true")) {
            	T.setHeader(header);
            }
            T.setRows(rows);
            table.setValue(T); 
            excelFile.close();
             
 //           execution.setVariable("Data",table);
                       
            log.info("*********************END-ReadXlsxFile**************************");
            log.info("Read XLS Sucessfull");
            return new Status("00","Process Sucessfull");  
            
        } catch (FileNotFoundException e) {
             try {
				excelFile.close();
			       return new Status("10","File Closed");
			} catch (IOException e1) {

				log.error("FileNotFound Error");
				return new Status("Error",e1.getMessage(),e1);
			}
        } catch (IOException e) {

            try {
				excelFile.close();
			       return new Status("10","File Closed");
			} catch (IOException e1) {

				return new Status("Error",e1.getMessage(),e1);
			}
        }catch (Exception e) {

            try {
				excelFile.close();
			       return new Status("00","File Closed");
			} catch (IOException e1) {
				return new Status("Error",e1.getMessage(),e1);
			}
        }
    }
	
}