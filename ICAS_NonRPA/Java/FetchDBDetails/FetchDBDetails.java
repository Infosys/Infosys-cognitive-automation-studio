/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.ConnectException;
import java.security.Timestamp;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.CreationHelper;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.camunda.bpm.engine.variable.value.ObjectValue;
import org.joda.time.DateTime;
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

@Bot(name = "FetchDBDetails", version = "1.0", description = "", botCategory = "String", author = "", technology = "Java", technologyCode = "01", botCategoryCode = "0A", botId = "0A")

public class FetchDBDetails {
	private static final Logger log = LoggerFactory.getLogger(FetchDBDetails.class);

	@Errors(exceptions = {
			@Error(errorCode = "010A0A11FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "010A0A1101", errorMessagePattern ="Folder Path Does Not Exist" , exceptionClass=IOException.class)})

	public Status execute(
			@InputParameter(name = "ExcelFilePath",constraints= { EXISTS, FOLDER}) String excelFilePath,
			@InputParameter(name = "Sql_Query") String sql_query,
			@InputParameter(name = "DB_Url") String db_url,
			@InputParameter(name = "User_Name") String user_name,
			@InputParameter(name = "Password") String pass_word,
			@OutputParameter(name = "FileStoragePath") ObjectHolder<String> fileStoragePath)
			throws ExecutionError, SQLException, IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA;
		String errorCodeB;
		String errorDescrption;
		
		if(db_url.equals(null))
		{
			errorCodeA="1";
			errorCategoryCode = "1";
			errorCodeB = "0D";
			errorDescrption = "Invalid Url";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + db_url);
		}
		

		
		try {
			ResultSet resultSet = null;
			DateFormat df = new SimpleDateFormat("dd/MM/yy");
			Date dateobj = new Date();
			String dateFormat = df.format(dateobj);
			String filePath = excelFilePath + "\\" + "result_" + DateTime.now().toString("yyyyMMddHHmmss") + ".xlsx";

			Connection connection = DriverManager.getConnection(db_url, user_name, pass_word);
			log.info("Connection created successfully" + connection);
			log.info("Fetching Details from DB............................................");
			Statement statement = connection.createStatement();

			resultSet = statement.executeQuery(sql_query);
			if (resultSet.getRow() < 0) {
				log.info("ResultSet in empty");
			} else {

				File f = new File(filePath);
				f.createNewFile();
				XSSFWorkbook workbook = new XSSFWorkbook();
				XSSFSheet sheet = workbook.createSheet("Sheet1");

				writeHeaderLine(resultSet, sheet);

				writeDataLines(resultSet, workbook, sheet);

				FileOutputStream outputStream = new FileOutputStream(filePath);
				workbook.write(outputStream);
				workbook.close();
				statement.close();

				log.info("File created");
				fileStoragePath.setValue(filePath);
			}
			return new Status("00", "Fetched the database successfully ");
			// Use relative path for Unix systems

		}catch (Exception e) {
			log.info("Input Output error:");
			e.printStackTrace();
			return new Status("Error",e.getMessage());
		}
		
	}

	private void writeHeaderLine(ResultSet result, XSSFSheet sheet) {
		ArrayList<String> columnList = new ArrayList<String>();

		try {
			ResultSetMetaData rsmd = result.getMetaData();
			int numberOfColumns = rsmd.getColumnCount();
			System.out.println(numberOfColumns);
			System.out.println(rsmd.getColumnName(2));
			for (int i = 1; i <= numberOfColumns; i++) {
				columnList.add(rsmd.getColumnName(i));
				System.out.println(rsmd.getColumnName(i));
				System.out.println(rsmd.getColumnClassName(i));

			}

			Row headerRow = sheet.createRow(0);
			Cell headerCell = headerRow.createCell(0);
			headerCell.setCellValue(columnList.get(0));
			for (int i = 1; i < columnList.size(); i++) {

				headerCell = headerRow.createCell(i);
				headerCell.setCellValue(columnList.get(i));
				System.out.println(headerCell.getStringCellValue());

			}
		} catch (SQLException e) {
			System.out.println("Sql Exception");
			e.printStackTrace();
		}
	}

	private void writeDataLines(ResultSet result, XSSFWorkbook workbook, XSSFSheet sheet) throws SQLException {
		Object cellData = null;
		int rowCount = 1;
		ResultSetMetaData rsmd = result.getMetaData();
		int numberOfColumns = rsmd.getColumnCount();
		while (result.next()) {
			Row row = sheet.createRow(rowCount++);
			int columnCount = 0;

			for (int i = 1; i <= numberOfColumns; i++) {

				Cell cell = row.createCell(columnCount++);
				cellData = result.getObject(rsmd.getColumnName(i));
				if (cellData instanceof String)
					cell.setCellValue((String) cellData);
				else if (cellData instanceof Integer)
					cell.setCellValue((Integer) cellData);
				else if (cellData instanceof Double)
					cell.setCellValue((Double) cellData);
				else if (cellData instanceof Float)
					cell.setCellValue((Float) cellData);

			}
		}
	}

}
