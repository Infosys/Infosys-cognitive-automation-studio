/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

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

@Bot(name = "CheckFileExists", version = "1.0", description = "", botCategory = "String", author = "", technology = "", technologyCode = "01", botCategoryCode = "01", botId = "09")

//ErrorCategory(ValidationError: 1, ConnectionError: 2,AccessError : 3, DiskIOError: 4, DBIOError: 5,
//NetworkIOError: 6, ConfigurationError: 7)
//botCode = technologyCode + categoryCode + botId
//botErrorCode = errorCategoryCode + errorCodeA + errorCodeB
//errorCode = botCode + botErrorCode 
//String botErrorCode;
//String errorCategoryCode;
//String errorCodeA = "1";
//String errorCodeB;
//String errorDescrption;

public class CheckFileExists {
	private static final Logger log = LoggerFactory.getLogger(CheckFileExists.class);

	@Errors(exceptions = {
			@Error(errorCode = "01010911FF", errorMessagePattern = ".*", exceptionClass = IOException.class), })

	public Status execute(@InputParameter(name = "SourcePath") String sourcePath,
			@InputParameter(name = "FileName") String fileName,
			@OutputParameter(name = "FileExists") ObjectHolder<String> fileExists
	) throws ExecutionError, IOException {
		try {
			String FilePath = sourcePath + "//" + fileName;

			log.info("FilePath :: " + FilePath);
			log.info("Filename :: " + fileName);
			File file = new File(FilePath);
			if (file.exists() && file.isFile())
				fileExists.setValue("true");
			else
				fileExists.setValue("false");
		} catch (Exception e) {
			log.info(e.getMessage());
			fileExists.setValue("false");
		}
		log.info("FileExists :: " + fileExists.getValue());
		return new Status("00", "FileExists " + fileExists.getValue());
	}

}
