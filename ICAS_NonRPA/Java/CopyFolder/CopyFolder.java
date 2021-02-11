/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;
import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

/*
 * Copy source folder to target folder
 */
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class CopyFolder  {
	private static final Logger log = LoggerFactory.getLogger(CopyFolder.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="SourceFolder", constraints= {FOLDER, EXISTS}) String sourceFolder,
			@InputParameter(name="TargetFolder") String targetFolder,
			@OutputParameter(name="CopiedFolder") ObjectHolder<String> copiedFolder
			) throws Exception {

		File sourceLocation = new File(sourceFolder);
		String folderName=sourceLocation.getName();
		File targetLocation = new File(targetFolder,folderName);
	
		try {
			copy(sourceLocation, targetLocation);
			copiedFolder.setValue(targetLocation.getPath());
			System.out.println(targetLocation.getPath());
			
			return new Status("00","CopiedFolder "+targetLocation.getPath());
		} catch (Exception e) {
			
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}

	
	}

	public static void copy(File sourceLocation, File targetLocation) {
		try {
				if (sourceLocation.isDirectory())
				{
						copyDirectory(sourceLocation, targetLocation);
				} else {
					copyFile(sourceLocation, targetLocation);
				}
					
				log.info("CopyFolder Successfull");
		} catch (Exception e) {

			log.error("Error occured while copying " + sourceLocation.getPath() + " to " + targetLocation.getPath());
			
		}
	}

	private static void copyDirectory(File source, File target) throws IOException {
		if (!target.exists()) {
			target.mkdir();
		}

		for (String f : source.list()) {
			copy(new File(source, f), new File(target, f));
		}
	}

	private static void copyFile(File source, File target) throws IOException {
		try (InputStream in = new FileInputStream(source); OutputStream out = new FileOutputStream(target)) {
			byte[] buf = new byte[1024 * 10];
			int length;
			while ((length = in.read(buf)) > 0) {
				out.write(buf, 0, length);
			}
		}
	}
}
