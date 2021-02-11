/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;


import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;
import static com.infosys.impact.botfactory.microbots.framework.Validation.NOT_NULL;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class WriteFile {
	private static final Logger log = LoggerFactory.getLogger(WriteFile.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="FileName",constraints= {NOT_NULL}) String fileName,
			@InputParameter(name="Source",constraints= {FOLDER, EXISTS}) String path,
			@InputParameter(name="Content") byte[] content
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			
			) throws Exception {

		File sourcefile = new File(path,fileName);
		
		if(!sourcefile.exists())
		{
			throw new ApplicationException("source file not exists").errorCode("SOURCE FILE NOT EXISTS");
			
		}
		
		try {
			
			FileOutputStream wr = new FileOutputStream(fileName);
			wr.write(content);
			wr.close();
			log.info("Write Successfull");
			return new Status("00","write File Success");
			
		} catch (IOException e) {
			
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);

		}
	}
}


