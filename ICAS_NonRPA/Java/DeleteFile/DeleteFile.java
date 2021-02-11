/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class DeleteFile {

	private static final Logger log = LoggerFactory.getLogger(DeleteFile.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="SourcePath", constraints= {FOLDER, EXISTS}) String sourcePath,
			@InputParameter(name="FileName", constraints= {FILE, EXISTS}) String fileName
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			
			) throws Exception {

		File file = new File(sourcePath, fileName);

		try {

			if (file.delete()) {

				log.info("**********************************************\n");
				log.info(fileName + " File deleted successfully");
				log.info("\n**********************************************");
				

			} else {
				log.info("Failed to delete the file");
			}
			
			return new Status("00","File deleted Successfully from ");
		} catch (Exception e) {

			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);

		}

	}

}
