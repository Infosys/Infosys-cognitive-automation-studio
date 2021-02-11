/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;
import static com.infosys.impact.botfactory.microbots.framework.Validation.NOT_NULL;

import java.io.FileWriter;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

//*****************************************************
//Input : Content of file, string to search and replacement string.
//Output : The content is replaced in the output file. 
//Description :  It reads the content of the file, searches the string and replaces the occurrences with the
//new string.The output is written into the file.
//*****************************************************

public class Replace  {
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	private static final Logger log = LoggerFactory.getLogger(Replace.class);

	public Status execute(
			@InputParameter(name="Content",constraints= {NOT_NULL}) String content,
			@InputParameter(name="StringPattern",constraints= {NOT_NULL}) String stringPattern,
			@InputParameter(name="NewValue",constraints= {NOT_NULL}) String newValue,
			@InputParameter(name="File",constraints= {FILE, EXISTS}) String file
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			) throws Exception {

		try {
			
		String replacedContent = content.replaceAll(stringPattern, "" + newValue);
			log.info("******** ReplacedContent is ::" + replacedContent);
			FileWriter fw = new FileWriter(file);
			fw.write(replacedContent);
			fw.close();
			log.info("Replace Successfull");
			return new Status("00","Replace Successfull");
		} catch (Exception e) {

			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);

		}

	}

}
