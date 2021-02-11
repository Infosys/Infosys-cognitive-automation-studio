/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.git;
/*
 * pull changes from git
 */
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

import com.infosys.impact.botfactory.custom.Utility;


public class GitPull  {
	private static final Logger log = LoggerFactory.getLogger(GitPull.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="GitLocalRepoPath") String gitLocalRepoPath
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files	
			) throws Exception {

		File workiFile = new File(gitLocalRepoPath);
		log.info("Pulling changes to" + workiFile);
		
		try {
			gitPull(workiFile);
			return new Status("00","Process Sucessfull");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}

	}

	public static void gitPull(File workiFile) {

		String command;
		command = "git pull";
		Utility.runProcess("", workiFile, command, true);

	}

}
