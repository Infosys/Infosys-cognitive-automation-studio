/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
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

@Bot(name = "ReadFile", version = "1.0", description = "", botCategory = "String", author = "",
        technology = "", technologyCode = "01", botCategoryCode = "01", botId = "05")

//ErrorCategory(ValidationError: 1, ConnectionError: 2,AccessError : 3, DiskIOError: 4, DBIOError: 5,
//NetworkIOError: 6, ConfigurationError: 7)
//botCode = technologyCode + categoryCode + botId
//botErrorCode = errorCategoryCode + errorCodeA + errorCodeB
//errorCode = botCode + botErrorCode ) 

public class ReadFile {
	private static final Logger log = LoggerFactory.getLogger(ReadFile.class);

	@Errors(exceptions = {
	        @Error(errorCode = "01010511FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
	        @Error(errorCode = "0101051101", errorMessagePattern = "Folder Path Does Not Exist", exceptionClass = IOException.class),
	        @Error(errorCode = "0101051105", errorMessagePattern = "Is Not Folder ", exceptionClass = IOException.class),
	        @Error(errorCode = "0101051103", errorMessagePattern = "File Does Not Exist", exceptionClass = IOException.class)
	})
	public Status execute(
	        @InputParameter(name = "FilePath") String filePath,
	        @InputParameter(name = "SourceFolder") String sourcePath,
	        @InputParameter(name = "FileName") String fileName,
	        @OutputParameter(name = "Content") ObjectHolder<String> content,
	        @OutputParameter(name = "ContentArray") ObjectHolder<byte[]> contentArray,
	        @OutputParameter(name = "File") ObjectHolder<String> file) throws ExecutionError, IOException {

		File source;
		if (filePath != null) {
			source = new File(filePath);
		} else {

			source = new File(sourcePath, fileName);
		}
		try {

			BufferedReader reader = new BufferedReader(new FileReader(source));
			StringBuffer sb = new StringBuffer();
			String l = null;
			do {

				l = reader.readLine();
				if (l != null) {
					sb.append(l + "\n");
					log.debug("*************************************************************************");
					log.debug(" Read  file :: " + sb);
					log.debug("*************************************************************************");

				}
			} while (l != null);
			reader.close();
			if (sb.toString().trim().length() >= 3500)
				content.setValue(sb.toString().trim().substring(0, 3500));
			else
				content.setValue(sb.toString().trim());
			contentArray.setValue(sb.toString().getBytes());
			file.setValue(filePath);
			log.info("Read file Success");
			return new Status("00", "Read file Success");
		}

		catch (IOException e) {

			e.printStackTrace();
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error", e.getMessage(), e);

		}

	}

}
