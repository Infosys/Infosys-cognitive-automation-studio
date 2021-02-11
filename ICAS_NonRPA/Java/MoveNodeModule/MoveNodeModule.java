/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

/*
 * Move node modules inside the app
 */
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class MoveNodeModule {

	private static final Logger log = LoggerFactory.getLogger(MoveNodeModule.class);

	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })
	public Status execute(
			@InputParameter(name = "TargetFolder", constraints = { FOLDER, EXISTS }) String targetFolder,
			@InputParameter(name = "FilePaths.TEMP") String source
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
	) throws Exception {

		File location = new File(source);
		String folder = folderList(location).get(0);

		try {
			if (!new File(targetFolder, "node_modules").exists()) {
				MoveFolder.moveTwoDirectories(targetFolder, null, new File(location, folder).getPath());

				new File(targetFolder, folder).renameTo(new File(targetFolder + "\\" + "node_modules"));
			}
			log.info("Node modules are moved to " + targetFolder);
			return new Status("00", "Node modules are moved to " + targetFolder);
		} catch (Exception e) {
			return new Status("Error", e.getMessage(), e);
		}

	}

	public static ArrayList<String> folderList(File location) {
		ArrayList<String> al = new ArrayList<String>();
		for (int i = 1; i <= 10; i++) {
			if (new File(location, "node_modules_" + i).exists()) {
				al.add("node_modules_" + i);
			}

		}
		return al;
	}

}
