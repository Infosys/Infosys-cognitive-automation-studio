/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import static com.infosys.impact.botfactory.microbots.framework.Validation.DOES_NOT_EXIST;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

/*
 * create folder inside parent folder
 */
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class CreateFolder {
	private static final Logger log = LoggerFactory.getLogger(CreateFolder.class);

	@Errors(exceptions = {
			@Error(errorCode = "010123456", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })
	public Status execute(

			@InputParameter(name = "ParentFolder", constraints = { FOLDER, DOES_NOT_EXIST }) String parentFolder

	) throws Exception {
		SimpleDateFormat df = new SimpleDateFormat("yyyyMMddhhmmss");
		String folderName = df.format(new Date());
		File folder = new File(parentFolder, folderName);

		try {
			folder.mkdir();
			log.info("Create Folder Successfull");
			return new Status("00", "Create Folder Successfull");
		} catch (Exception e) {
			log.info("Display Error code ::");
			return new Status("Error", e.getMessage(), e);
		}
	}
}
