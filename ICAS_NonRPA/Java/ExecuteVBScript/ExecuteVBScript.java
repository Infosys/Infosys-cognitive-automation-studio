/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;

import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "ExecuteVBScript", version = "1.0", description = "", botCategory = "File", author = "",
	technology = "", technologyCode = "01", botCategoryCode = "01", botId = "07")


public class ExecuteVBScript {
	private static final Logger log = LoggerFactory.getLogger(ExecuteVBScript.class);

	@Errors(exceptions = {
			@Error(errorCode = "01010711FF", errorMessagePattern = ".*", exceptionClass = IOException.class) })

	public Status execute(
			@InputParameter(name = "ScriptFile", constraints = { EXISTS }) String scriptFile,
			@InputParameter(name = "ExecutablePath", constraints = { EXISTS }) String executablePath
			
	) throws ExecutionError, IOException {
	
		try {
			 //scriptFile = "C:\\work\\selenium\\chrome\\test.vbs";
			//executablePath = "C:\\windows\\...\\vbs.exe"; 
			String cmdArr [] = {executablePath, scriptFile};
			Runtime.getRuntime ().exec (cmdArr);
			return new Status("00",	"executed VB Script file Successfully  ");
		} catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}

	}

}
