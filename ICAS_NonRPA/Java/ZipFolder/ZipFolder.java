/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.*;
import java.util.zip.*;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "ZipFolder", version = "1.0", description = "", botCategory = "Folder", author = "", technology = "", technologyCode = "01", botCategoryCode = "02", botId = "01")

public class ZipFolder {
	private static final Logger log = LoggerFactory.getLogger(ZipFolder.class);

	@Errors(exceptions = {
			@Error(errorCode = "01020111FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0102011101", errorMessagePattern = "Folder Path Does Not Exist", exceptionClass = IOException.class),
			@Error(errorCode = "0102011105", errorMessagePattern = "Source Is Not Folder ", exceptionClass = IOException.class) })

	public Status execute(@InputParameter(name = "FolderPath", constraints = { EXISTS, FOLDER, }) String folderPath,
			@InputParameter(name = "ZipFilePath", constraints = {}) String zipFilePath,
			@OutputParameter(name = "ZippedFilePath") ObjectHolder<String> zippedFilePath)
			throws ExecutionError, IOException {

		System.out.println("Folder to be Zipped present at path: " + folderPath);

		try {
			File srcFile = new File(folderPath);
			String zipPath = zipFilePath+".zip";
			File[] files = srcFile.listFiles();
			FileOutputStream fos = new FileOutputStream(zipPath);
			ZipOutputStream zos = new ZipOutputStream(fos);
			for (int i = 0; i < files.length; i++) {

				byte[] buffer = new byte[1024];
				FileInputStream fis = new FileInputStream(files[i]);
				zos.putNextEntry(new ZipEntry(files[i].getName()));
				int length;
				while ((length = fis.read(buffer)) > 0) {
					zos.write(buffer, 0, length);
				}
				zos.closeEntry();
				fis.close();
			}
			zos.close();
			System.out.println("Zipped folder at location :"+zipPath);
			zippedFilePath.setValue("File Zipped at: "+zipPath);
			return new Status("00", "Zipped Folder Successfully at:  " + zipPath);
		}

		catch (Exception e) {
			System.out.println("Some error occured: " + e.getMessage().toString());
			zippedFilePath.setValue("Some error occured");
			return new Status("00", "Some error occured: " + e.getMessage().toString());
		}
	}

}
