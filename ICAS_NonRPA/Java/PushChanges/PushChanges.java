/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.git;

import java.io.File;
import java.io.IOException;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.eclipse.jgit.api.errors.GitAPIException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.custom.Utility;

/*
 * push changes that are commited to git
 */
public class PushChanges  {
	private static final Logger log = LoggerFactory.getLogger(PushChanges.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="CloneFolderPath") String cloneFolderPath
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			) throws Exception {

		File workiFile = new File(cloneFolderPath);
		log.info("Pushing changes for " + workiFile);

		try {
			pushChanges(workiFile);
			return new Status("00","Process Sucessfull");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}
	}

	public static void pushChanges(File workiFile) throws GitAPIException {

		String command;
		command = "git checkout";
		Utility.runProcess("", workiFile, command, true);

		command = "git push origin master";
		Utility.runProcess("", workiFile, command, true);

	}

}
