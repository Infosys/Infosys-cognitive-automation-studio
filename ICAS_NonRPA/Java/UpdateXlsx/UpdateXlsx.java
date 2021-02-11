/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.excel;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.custom.table.Table;

public class UpdateXlsx {
	private static final Logger log = LoggerFactory.getLogger(UpdateXlsx.class);

	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })
	public Status execute(
			@InputParameter(name = "filepath") String fileName,
			@InputParameter(name = "Table") Table table
			) 	throws Exception {
		
		log.info("*********************UpdateXlsx**************************");

		XSSFWorkbook workbook = new XSSFWorkbook();
		XSSFSheet sheet = workbook.createSheet("Incidents");
		int rowNum = 0;

		for (int i = 0; i < table.getRows().size(); i++) {
			// log.info("Row-("+i+")---------------------->"+table.getRows().get(i).getCells());
			Row currentRow = sheet.createRow(rowNum++);
			int colNum = 0;
			for (int j = 0; j < table.getRows().get(i).getCells().size(); j++) {
				Cell cell = currentRow.createCell(colNum++);
				// log.info("Cell-("+j+")---------------------->"+table.getRows().get(i).getCells().get(j));

				if (currentRow.getRowNum() > 0) {
					if (cell.getColumnIndex() == 0) {
						Object field = table.getRows().get(i).getCells().get(j);
						if (field instanceof String) {
							cell.setCellValue((String) field);
						} else if (field instanceof Integer) {
							cell.setCellValue((Integer) field);
						}
					} else if (cell.getColumnIndex() == 1) {
						cell.setCellValue("Awaiting User Confrmation");
					} else if (cell.getColumnIndex() == 2) {
						cell.setCellValue(
								"Restarted the server service on the file server. Please try now and let us know if the issue persists");
					}

				} else {
					if (cell.getColumnIndex() == 0) {
						cell.setCellValue("Name");
					} else if (cell.getColumnIndex() == 1) {
						cell.setCellValue("State");
					} else if (cell.getColumnIndex() == 2) {
						cell.setCellValue("Closure Comments");
					}
				}

			}
		}

		try {
			FileOutputStream outputStream = new FileOutputStream(fileName);
			workbook.write(outputStream);
			workbook.close();
			outputStream.close();
			log.info("Update xls Sucessfull");
			return new Status("00", "Process Sucessfull");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			return new Status("Error", e.getMessage(), e);
		} catch (IOException e) {
			e.printStackTrace();
			return new Status("Error", e.getMessage(), e);
		}
	}

}
