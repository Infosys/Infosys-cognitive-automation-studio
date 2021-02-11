/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;


//import java.io.IOException;

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

@Bot(name = "PrintWord", version = "1.0", description = "", botCategory = "String", author = "",
	technology = "", technologyCode = "01", botCategoryCode = "06", botId = "04")

//ErrorCategory(ValidationError: 1, ConnectionError: 2,AccessError : 3, DiskIOError: 4, DBIOError: 5,
//               NetworkIOError: 6, ConfigurationError: 7)
//botCode = technologyCode + categoryCode + botId
//botErrorCode = errorCategoryCode + errorCodeA + errorCodeB
//errorCode = botCode + botErrorCode  

public class PrintWord {
	private static final Logger log = LoggerFactory.getLogger(PrintWord.class);

	@Errors(exceptions = {
			@Error(errorCode = "01060411FF", errorMessagePattern = ".*", exceptionClass = Exception.class),
			@Error(errorCode = "0106041111", errorMessagePattern = "Field value Null", exceptionClass = Exception.class) })

	public Status execute(
			@InputParameter(name = "inputWord") String word
			//@OutputParameter(name="ord") ObjectHolder<String> fileToCopy
			
	) throws ExecutionError, Exception {

		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA = "1";
		String errorCodeB;
		String errorDescrption;

		if (word==null) {

			errorCategoryCode = "1";
			errorCodeB = "11";
			errorDescrption = "Field value Null";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + word);

		}

		log.info("Starting process....");

		try {
			System.out.print("input word is:"+word);
			log.info("input word is:"+word);
			log.info("Printed Successfully");
			return new Status("00",	"Printed Successfully");
		} catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}

	}

}
