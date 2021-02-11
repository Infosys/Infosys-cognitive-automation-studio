/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.git;

/*
 * To add files into git stagging area
 */

import java.io.File;
import java.io.IOException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AddFileToIndex  {
	private static final Logger log = LoggerFactory.getLogger(AddFileToIndex.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="GitLocalRepositoryPath") String gitLocalRepositoryPath
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files	
			) throws Exception {		
				File gitLocalRepo = new File(gitLocalRepositoryPath + "\\.git");
				log.info("Adding changed files of " + gitLocalRepositoryPath + " to stagged area");
				try {
					addFileToIndex(gitLocalRepo);
					log.info("Changed files of " + gitLocalRepositoryPath + " are added to stagged area");
					return new Status("00","Process Sucessfull");
				} catch (Exception e) {
					return new Status("Error",e.getMessage(),e);
				}
			}

	public static void addFileToIndex(File gitLocalRepo)
			throws IOException, GitAPIException {
				Git reGit = Git.open(gitLocalRepo);
				reGit.add().addFilepattern(".").call();
	       }
}
