/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.git;

/*
 * To  clone  the project from git to local machine
 * RepositoryUrl is user specific.
 * Project name in git should be same as application created
 */
import java.io.File;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.util.Arrays;
import java.util.Comparator;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class CloneRepo {
	private static final Logger log = LoggerFactory.getLogger(CloneRepo.class);

	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })
	public Status execute(
			@InputParameter(name = "GitUrl") String repositoryUrl,
			@InputParameter(name = "GitLocalRepositoryPath") String gitLocalRepositoryPath,
			@OutputParameter(name = "GitClonedFolder") ObjectHolder<String> gitClonedFolder

	) throws Exception {

		log.info("Git url is :: " + repositoryUrl);
		log.info("Cloning Project " + repositoryUrl + " to " + gitLocalRepositoryPath);

		String command;
		command = "git clone " + repositoryUrl;

		File workingDir = new File(gitLocalRepositoryPath);
		if (!workingDir.exists()) {
			workingDir.mkdir();
		}

		try {
			ExecuteCommand(workingDir, command);

			File[] files = workingDir.listFiles();
			File lastModified = Arrays.stream(files).filter(File::isDirectory).max(Comparator.comparing(File::lastModified))
					.orElse(null);
			String clonedFolderPath = lastModified.getPath();
			gitClonedFolder.setValue(clonedFolderPath);

			log.info("Cloning of Project " + repositoryUrl + "is completed at location " + gitLocalRepositoryPath);
			return new Status("00", "Process Sucessfull");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}
	}

	private static void ExecuteCommand(File workingDir, String command) {
		try {
			ProcessBuilder pb = new ProcessBuilder(command.split(" ")).directory(workingDir);
			pb.redirectError(Redirect.INHERIT);
			pb.redirectOutput(Redirect.INHERIT);
			pb.redirectInput(Redirect.INHERIT);
			Process p = pb.start();

			p.waitFor();
		} catch (Exception e) {
			e.printStackTrace();

		}

	}

}
