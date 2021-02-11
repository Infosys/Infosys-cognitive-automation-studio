/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;
import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.apache.commons.io.FileUtils;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.Writer;

public class CsvToHtml {
		private static final Logger log = LoggerFactory.getLogger(CsvToHtml.class);
		
		@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
		
 public Status execute(
			@InputParameter(name="csvFilePath") String csvFilePath,
			@InputParameter(name="htmlFilePath") String htmlFilePath,
			@InputParameter(name="fileName") String fileName
			) throws Exception {
				
	
			try { 
			StringBuilder stringBuilder= new StringBuilder();
	 
			stringBuilder.append("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">");
			stringBuilder.append("<html xmlns=\"http://www.w3.org/1999/xhtml\">");
			stringBuilder.append("<head><meta http-equiv=\"Content-type\" content=\"text/html;charset=UTF-8\"/>");
			stringBuilder.append("<title>Csv2Html</title>");
			stringBuilder.append("<style type=\"text/css\">");
			stringBuilder.append("body{background-color:#FFF;color:#000;font-family:OpenSans,sans-serif;font-size:10px;}");
			stringBuilder.append("table{border:0.2em solid #2F6FAB;border-collapse:collapse;}");
			stringBuilder.append("th{border:0.15em solid #2F6FAB;padding:0.5em;background-color:#E9E9E9;}");
			stringBuilder.append("td{border:0.1em solid #2F6FAB;padding:0.5em;background-color:#F9F9F9;}</style>");
			stringBuilder.append("</head><body><h1>Csv2Html</h1>");
	 
			stringBuilder.append("<table>");
			//FileReader filereader = new FileReader("D:/supplier.csv"); 
			FileReader filereader = new FileReader(csvFilePath); 
	        // create csvReader object passing 
	        // file reader as a parameter 
	        BufferedReader br = new BufferedReader(filereader);
			String stdinLine;
			boolean firstLine = true;
			while ((stdinLine = br.readLine()) != null) {
				String[] columns = escapeChars(stdinLine).split(",");
				if ( firstLine == true) {
					tableHeader(stringBuilder, columns);
					firstLine = false;
				} else {
					tableRow(stringBuilder, columns);
				}
			}
			stringBuilder.append("</table></body></html>");
			//System.out.println(stringBuilder);
			 WriteToFile(stringBuilder.toString(),htmlFilePath,fileName+".html");
			 return new Status("00","HtmlFile created in "+htmlFilePath);
		}catch (IOException e) {
	       String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className );
			return new Status("Error",e.getMessage(),e);

		}
		}
		
		public static void WriteToFile(String fileContent, String source,String fileName) throws IOException {
		    //String projectPath = System.getProperty("user.dir");
			String projectPath=source;
		    String tempFile = projectPath + File.separator+fileName;
		    File file = new File(tempFile);
		    // if file does exists, then delete and create a new file
		    if (file.exists()) {
		        try {
		            File newFileName = new File(projectPath + File.separator+ "backup_"+fileName);
		            file.renameTo(newFileName);
		            file.createNewFile();
		        } catch (IOException e) {
		            e.printStackTrace();
		        }
		    }
		    //write to file with OutputStreamWriter
		    OutputStream outputStream = new FileOutputStream(file.getAbsoluteFile());
		    Writer writer=new OutputStreamWriter(outputStream);
		    writer.write(fileContent);
		    writer.close();

			



			}
			
		
	
	   
	
	public static String escapeChars(String lineIn) {
		StringBuilder sb = new StringBuilder();
		int lineLength = lineIn.length();
		for (int i = 0; i < lineLength; i++) {
			char c = lineIn.charAt(i);
			switch (c) {
				case '"': 
					sb.append("&quot;");
					break;
				case '&':
					sb.append("&amp;");
					break;
				case '\'':
					sb.append("&apos;");
					break;
				case '<':
					sb.append("&lt;");
					break;
				case '>':
					sb.append("&gt;");
					break;
				default: sb.append(c);
			}
		}
		return sb.toString();
	}
 
	public static void tableHeader(StringBuilder stringBuilder, String[] columns) {
		stringBuilder.append("<tr>");
		for (int i = 0; i < columns.length; i++) {
			stringBuilder.append("<th>");
			stringBuilder.append(columns[i]);
			stringBuilder.append("</th>");
		}
		stringBuilder.append("</tr>");
	}
 
	public static void tableRow(StringBuilder stringBuilder, String[] columns) {
		stringBuilder.append("<tr>");
		for (int i = 0; i < columns.length; i++) {
			stringBuilder.append("<td>");
			stringBuilder.append(columns[i]);
			stringBuilder.append("</td>");
		}
		stringBuilder.append("</tr>");
	}
	
}
