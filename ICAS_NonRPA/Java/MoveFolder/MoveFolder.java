/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;
/*
 * Move a folder
 */

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class MoveFolder {
	private static final Logger log = LoggerFactory.getLogger(MoveFolder.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="TargetPath") String targetPath,
			@InputParameter(name="TargetFolder", constraints= {FOLDER, EXISTS}) String targetFolder,
			@InputParameter(name="SourceFolder", constraints= {FOLDER, EXISTS}) String source
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			) throws Exception {

		try {
			moveTwoDirectories(targetPath, targetFolder, source);
			log.info("Move Folder successful");
			return new Status("00","Folder Moved Successfully ");

		} 		
		catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);			
		}

	}

	public static void moveTwoDirectories(String targetPath, String targetFolder, String source) {

		if (source != null) {
			File sourceFolder = new File(source);
			if (!sourceFolder.exists()) {
				log.error("The source Folder " + sourceFolder.getPath() + " does not exits");
			} else {

				String folderName = sourceFolder.getName();
				if (targetPath == null) {
					if (new File(targetFolder).getName() != sourceFolder.getName()) {

						sourceFolder
								.renameTo(new File(new File(targetFolder).getParent() + File.separator + folderName));
					} else {
						log.error("The target Folder name and source folder name are same");
					}

				} else if (targetFolder == null) {
					if (new File(targetPath, folderName).exists()) {
						log.error("The source Folder already exists in the target path provided");

					} else
						sourceFolder.renameTo(new File(targetPath + File.separator + folderName));

				} else {
					log.error("Please provide a target Folder or target path");
				}
			}
		} else {
			log.error("Please provide a source folder");
		}

		// check if node modules exits. copy entire folder directly

	}
}
