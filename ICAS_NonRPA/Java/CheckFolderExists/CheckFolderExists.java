/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class CheckFolderExists  {
	private static final Logger log = LoggerFactory.getLogger(CheckFolderExists.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})

	public Status execute(
			@InputParameter(name="FolderPath") String folder,
			@OutputParameter(name="FolderExists") ObjectHolder<String> folderExists
			
			) throws Exception {

		log.info("Foldername :: "+folder);
		if (new File(folder).exists())
			folderExists.setValue("true");

		else
			folderExists.setValue("false");
		log.info("FolderExists :: "+folderExists.getValue());
		return new Status("00","FolderExists "+folderExists.getValue());
	}
	

}
