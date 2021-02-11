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


public class CopyFile {	
	private static final Logger log = LoggerFactory.getLogger(CopyFile.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		}) 
	public Status execute(
			@InputParameter(name="Source",constraints= {FOLDER, EXISTS}) String source,
			@InputParameter(name="Target",constraints= {FOLDER, EXISTS}) String target,
			@InputParameter(name="FileName",constraints= {FILE, EXISTS}) String fileName
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			) throws Exception {
		
		File sourceFile = new File(source , fileName);
		String name = sourceFile.getName();		
		File targetFile = new File(target + File.separator + name);
		log.info("Copy File Details...." + fileName);
		
		try {
			FileUtils.copyFile(sourceFile, targetFile);
			log.info("Copy Successfull");
			return new Status("00","Copied file Successfully from "+sourceFile.getPath()+" to "+targetFile.getPath());
			
		} catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className );
			return new Status("Error",e.getMessage(),e);
			
		}
	}
}
