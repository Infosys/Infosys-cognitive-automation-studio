/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.git;

/*
 * To commit stagged changes of git project
 */
import java.io.File;
import java.io.IOException;
import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.eclipse.jgit.api.CommitCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CommitChanges  {
	private static final Logger log = LoggerFactory.getLogger(CommitChanges.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="GitLocalRepoPath") String gitLocalRepoPath,
			@InputParameter(name="CommitMessage") String commitMessage
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files	
			) throws Exception {

		File gitLocalRepo = new File(gitLocalRepoPath);
		log.info("Commiting the stagged changes of " + gitLocalRepoPath + " the commit message is " + commitMessage);

		try {
			commitChanges(gitLocalRepo, commitMessage);
			log.info("Stagged changes are commited");
			return new Status("00","Process Sucessfull");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}
	 	}

	public static void commitChanges(File gitLocalRepo, String commitMessage)
			throws GitAPIException {
		Git reGit;
		try {
			reGit = Git.open(gitLocalRepo);
			CommitCommand commit = reGit.commit();
			commit.setAllowEmpty(true);
			commit.setMessage(commitMessage).call();

		} catch (IOException e) {

			e.printStackTrace();
		}

	}
}
