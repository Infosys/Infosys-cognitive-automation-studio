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
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Calendar;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class CutPasteFile {

	private static final Logger log = LoggerFactory.getLogger(CutPasteFile.class);

	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })
	public Status execute(
			@InputParameter(name = "Source", constraints = { FOLDER, EXISTS }) String sourcePath,
			@InputParameter(name = "FileName", constraints = { FILE, EXISTS }) String fileName,
			@InputParameter(name = "Target", constraints = { FOLDER, EXISTS }) String targetPath,
			@InputParameter(name = "IsArchive") String archiveFlag
			) throws Exception {

		String source = sourcePath + File.separator + fileName;
		String target = targetPath + File.separator + fileName;

		File targetPathFile = new File(targetPath, fileName);
		Path result = null;
		// TODO provide option to decide whether to overwrite/append file when it exist
		try {
			if (targetPathFile.exists()) {
				targetPathFile.delete();
				result = Files.move(Paths.get(source), Paths.get(target));
			} else {
				if (archiveFlag.equalsIgnoreCase("true")) {

					File afile = new File(sourcePath + "/" + fileName);

					if (afile.renameTo(new File(
							targetPath + "/" + afile.getName() + "." + Calendar.getInstance().getTimeInMillis()))) {
						log.debug("File is moved successful!");
						

					} else {
						log.debug("File is failed to move!");
					}

				} else {
					result = Files.move(Paths.get(source), Paths.get(target));

				}

			}

			if (result != null || archiveFlag.equalsIgnoreCase("true")) {
				log.info("File moved successfully.");
				
			} else {
				log.warn("File movement failed.");
			}
			
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}
		return new Status("00","File moved successfully");
	}

}
