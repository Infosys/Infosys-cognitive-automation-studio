/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

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

@Bot(name = "DeleteTempFiles", version = "1.0", description = "", botCategory = "File", author = "", technology = "Java", technologyCode = "01", botCategoryCode = "01", botId = "0A")

public class UpdateFileInFolder {
	private static final Logger log = LoggerFactory.getLogger(UpdateFileInFolder.class);

	@Errors(exceptions = {
			@Error(errorCode = "01011411FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0101141103", errorMessagePattern = "File Does Not Exist", exceptionClass = IOException.class) })

	public Status execute(
			@InputParameter(name = "SourceFilePath", constraints = { EXISTS, FILE }) String sourceFilePath,
			@InputParameter(name = "DestFilePath", constraints = { EXISTS, FILE }) String destFilePath)
			throws ExecutionError, IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA;
		String errorCodeB;
		String errorDescrption;

		if (sourceFilePath.equals(null)) {
			errorCodeA = "1";
			errorCategoryCode = "1";
			errorCodeB = "03";
			errorDescrption = "Invalid File path";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + sourceFilePath);
		}

		InputStream is = null;
		OutputStream os = null;
		try {

			is = new FileInputStream(sourceFilePath);

			os = new FileOutputStream(destFilePath);

			byte[] buf = new byte[1024];
			int bytesRead;
			while ((bytesRead = is.read(buf)) > 0) {
				os.write(buf, 0, bytesRead);
			}

			is.close();
			os.close();
			System.out.println("Updated the file successfully");
			log.info("File is updated........");
			return new Status("00", "Updated the file successfully");
		} catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error", e.getMessage(), e);
		}

	}

}
