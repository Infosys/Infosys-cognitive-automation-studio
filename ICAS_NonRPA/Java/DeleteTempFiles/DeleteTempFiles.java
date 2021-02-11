/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;
import java.io.File;
import java.io.IOException;
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

public class DeleteTempFiles {
	private static final Logger log = LoggerFactory.getLogger(DeleteTempFiles.class);

	@Errors(exceptions = {
			@Error(errorCode = "01011311FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0101131101", errorMessagePattern = "Folder Path Does Not Exist", exceptionClass = IOException.class) })

	public Status execute(
			@InputParameter(name = "TempFolderPath", constraints = { EXISTS, FOLDER }) String tempFolderPath)
			throws ExecutionError, IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA;
		String errorCodeB;
		String errorDescrption;

		if (tempFolderPath.equals(null)) {
			errorCodeA = "1";
			errorCategoryCode = "1";
			errorCodeB = "01";
			errorDescrption = "Folder Path Does Not Exist";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + tempFolderPath);
		}

		try {

			File file = new File(tempFolderPath);
			deleteFolder(file);
			System.out.println("Deleted temp files successfully");
			log.info("Files deleted........");
			return new Status("00", "Deleted temp files successfully");

		} catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error", e.getMessage(), e);
		}

	}

	private void deleteFolder(File file) {
		try {
			for (File subFile : file.listFiles()) {
				if (subFile.isDirectory()) {
					deleteFolder(subFile);
					subFile.delete();
				} else {
					subFile.delete();
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
