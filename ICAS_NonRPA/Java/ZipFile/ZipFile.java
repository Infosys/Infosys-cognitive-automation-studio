/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.*;
import java.util.zip.*;

import org.apache.commons.io.FileUtils;
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

@Bot(name = "ZipFile", version = "1.0", description = "", botCategory = "File", author = "", technology = "", technologyCode = "01", botCategoryCode = "01", botId = "01")

public class ZipFile {
	private static final Logger log = LoggerFactory.getLogger(ZipFile.class);

	@Errors(exceptions = {
			@Error(errorCode = "01010111FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0101011101", errorMessagePattern = "File Path Does Not Exist", exceptionClass = IOException.class), })

	public Status execute(@InputParameter(name = "FilePath", constraints = { EXISTS }) String filePath,
			@OutputParameter(name = "ZippedFilePath") ObjectHolder<String> zippedFilePath)
			throws ExecutionError, IOException {

		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA = "1";
		String errorCodeB;
		String errorDescrption;
		File file = new File(filePath);
		if (!file.exists()) {
			errorCategoryCode = "1";
			errorCodeB = "03";
			errorDescrption = "File Does Not Exist";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + filePath);
		}
		System.out.println("File to be zipped present at path: " + filePath);
		String zipFile = filePath+".zip";
		try {
		    byte[] buffer = new byte[1024];
		    FileOutputStream fos = new FileOutputStream(zipFile);
		    ZipOutputStream zos = new ZipOutputStream(fos);         
		    File srcFile = new File(filePath);
		    FileInputStream fis = new FileInputStream(srcFile);
		    zos.putNextEntry(new ZipEntry(srcFile.getName()));          
		    int length;
		    while ((length = fis.read(buffer)) > 0) {
		        zos.write(buffer, 0, length);
		    }
		    zos.closeEntry();
		    fis.close();
		    zos.close(); 
		    zippedFilePath.setValue(zipFile);
		    System.out.println("File Zipped at: " + zipFile);
		    return new Status("00", "Zip file Successfully from " + zipFile);
		    
		}
		catch (IOException ioe) {
		    System.out.println("Error creating zip file" + ioe);
		    zippedFilePath.setValue("Error creating zip file" + ioe);
		    return new Status("00", "Error creating zip file" + ioe);
		}
	}

}
