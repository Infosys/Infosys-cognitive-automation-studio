/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

//*****************************************************
//Input : Folder location to be searched
//Input : Pattern to be searched
//Output : List of path of files for the corresponding pattern
//Description : it read folder location and the pattern. it searches the folder for the pattern specified.
//The output is list of path of files where the pattern matches.  
//*****************************************************
@Bot(name = "ListFiles", version = "1.0", description = "", botCategory = "String", author = "", technology = "", technologyCode = "01", botCategoryCode = "01", botId = "03")

//ErrorCategory(ValidationError: 1, ConnectionError: 2,AccessError : 3, DiskIOError: 4, DBIOError: 5,
//NetworkIOError: 6, ConfigurationError: 7)
//botCode = technologyCode + categoryCode + botId
//botErrorCode = errorCategoryCode + errorCodeA + errorCodeB
//errorCode = botCode + botErrorCode )

public class ListFiles {
	private static final Logger log = LoggerFactory.getLogger(ListFiles.class);

	@Errors(exceptions = {
			@Error(errorCode = "01010311FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0101031101", errorMessagePattern = "Folder Path Does Not Exist", exceptionClass = IOException.class),
			@Error(errorCode = "0101031105", errorMessagePattern = "Is Not Folder ", exceptionClass = IOException.class)

	})

	public Status execute(@InputParameter(name = "FolderPath", constraints = { EXISTS, FOLDER }) String folder,
			@InputParameter(name = "Pattern") String pattern,
			@InputParameter(name = "ModifiedAfter", required = false) String modifiedAfter,
			@OutputParameter(name = "Files") ObjectHolder<List<String>> files) throws Exception {
//		String botErrorCode;
//		String errorCategoryCode;
//		String errorCodeA = "1";
//		String errorCodeB;
//		String errorDescrption;

		long date = Long.MIN_VALUE;

		pattern = pattern.replaceAll("\\.", "\\\\.");
		pattern = pattern.replaceAll("\\*", ".*");
		log.info("ListFiles updated pattern = " + pattern);
		File folderToRead = new File(folder);

		List<String> files1 = new ArrayList<>();
		if (modifiedAfter != null) {
			date = new SimpleDateFormat("yyyyMMddHHmmss").parse(modifiedAfter).getTime();
			listFiles(folderToRead, files1, pattern, date);
			files.setValue(files1);
		} else {
			listFiles(folderToRead, files1, pattern);
			files.setValue(files1);
		}
		log.info("List file Successfull");
		return new Status("00", "List file Successfully from " + folder);
	}

	public static void listFiles(File folder, List<String> files, String pattern, long date) {
		for (final File fileEntry : folder.listFiles()) {
			if (fileEntry.isDirectory()) {
				listFiles(fileEntry, files, pattern, date);
			} else {
				if (fileEntry.getName().matches(pattern) && fileEntry.lastModified() > date) {
					log.debug("Entry " + fileEntry.getName() + " matches with pattern " + pattern);
					files.add(fileEntry.getPath());
				} else {
					log.debug("Entry " + fileEntry.getName() + " does not match with pattern " + pattern);
				}
			}
		}
	}

	public static void listFiles(File folder, List<String> files, String pattern) {
		for (final File fileEntry : folder.listFiles()) {
			if (fileEntry.isDirectory()) {
				listFiles(fileEntry, files, pattern);
			} else {
				if (fileEntry.getName().matches(pattern)) {
					log.debug("Entry " + fileEntry.getName() + " matches with pattern " + pattern);
					files.add(fileEntry.getPath());
				} else {
					log.debug("Entry " + fileEntry.getName() + " does not match with pattern " + pattern);
				}
			}
		}
	}

}
