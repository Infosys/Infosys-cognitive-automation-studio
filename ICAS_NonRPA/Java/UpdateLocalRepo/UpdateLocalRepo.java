/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.git;

import java.io.File;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.util.Arrays;
import java.util.Comparator;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
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

public class UpdateLocalRepo  {
	private static final Logger log = LoggerFactory.getLogger(UpdateLocalRepo.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="GitUrl") String repositoryUrl,
			@InputParameter(name="GitLocalRepositoryPath") String gitLocalRepositoryPath,
			@OutputParameter(name = "GitClonedFolder") ObjectHolder<String> gitClonedFolder
			) throws Exception {
		
		String repoProject = repositoryUrl.split("/")[repositoryUrl.split("/").length - 1].split("\\.")[0];
		if (!new File(gitLocalRepositoryPath).exists()) {
			new File(gitLocalRepositoryPath).mkdir();
		}
		String command = null;
		try {
			if (!new File(gitLocalRepositoryPath, repoProject).exists()) {
				log.info("git local repository doesn't exists:: initiating cloning");
				
				command = "git clone " + repositoryUrl;
				Utility.runProcess("", new File(gitLocalRepositoryPath), command, true);

			} else {
				log.info("git local repository exists:: fetching updates");
				command = "git pull";
				Utility.runProcess("", new File(gitLocalRepositoryPath, repoProject), command, true);
			}

			gitClonedFolder.setValue(new File(gitLocalRepositoryPath, repoProject).getPath());
			return new Status("00","Process Sucessfull");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			return new Status("Error",e.getMessage(),e);
		} 

	}

}
