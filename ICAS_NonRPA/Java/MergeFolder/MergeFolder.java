/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

/*
 * Merge two folders.
 * target folder will contains updated files of source and target
 */
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class MergeFolder {
	private static final Logger log = LoggerFactory.getLogger(MergeFolder.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="SourceFolder", constraints= {FOLDER, EXISTS}) String sourceFolder,
			@InputParameter(name="TargetFolder" ) String targetFolder
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			)  {

		try {

			File sourceLocation = new File(sourceFolder);
			File targetLocation = new File(targetFolder);
			merge(sourceLocation, targetLocation);
			log.info("Merge Folder successful");
			return new Status("00","Merge Folder successful ");
		} catch (Exception e) {


			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}

	}

	public static void merge(File srcFolder, File destFolder) {

		// make sure source exists
		if (!srcFolder.exists()) {

			log.info("Directory does not exist.");
			// just exit
			// System.exit(0);

		} else {

			try {

				copyFolder(srcFolder, destFolder);
			} catch (Exception e) {
				e.printStackTrace();
				
			}
		}

	}

	public static boolean fileCheck(File src, File dest) {
		boolean flag = true;

		File destFile = dest.getParentFile();

		if (src != null && dest != null) {
			int counter = 0;
			for (File destFileEntry : destFile.listFiles()) {
				counter++;
				if ((src.getName().equals(destFileEntry.getName())
						&& src.lastModified() <= destFileEntry.lastModified())) {

					flag = false;
					break;

				} else if ((src.getName().equals(destFileEntry.getName())
						&& src.lastModified() > destFileEntry.lastModified())) {

					flag = true;
					break;
				} else if (counter == destFile.listFiles().length && !(src.getName().equals(destFileEntry.getName()))) {
					flag = true;
					break;

				} else
					continue;

			}

		}
		return flag;
	}

	public static void copyFolder(File src, File dest) throws IOException {

		if (src.isDirectory()) {

			// if directory not exists, create it
			if (!dest.exists()) {
				dest.mkdir();
				log.info("Directory copied from " + src + "  to " + dest);
			}

			// list all the directory contents
			String files[] = src.list();

			for (String file : files) {
				// construct the src and dest file structure
				File srcFile = new File(src, file);
				File destFile = new File(dest, file);
				// recursive copy

				copyFolder(srcFile, destFile);
			}

		} else {
			// if file, then copy it
			// Use bytes stream to support all file types

			if (fileCheck(src, dest)) {

				InputStream in = new FileInputStream(src);
				OutputStream out = new FileOutputStream(dest);

				byte[] buffer = new byte[1024];

				int length;
				// copy the file content in bytes
				while ((length = in.read(buffer)) > 0) {
					out.write(buffer, 0, length);
				}

				in.close();
				out.close();
				log.info("File copied from " + src + " to " + dest);
			}

		}
	}

}
