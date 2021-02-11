/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.ftp;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;

import java.io.IOException;

import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPReply;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;


public class FTPFileDelete  {

	private static final Logger log = LoggerFactory.getLogger(FTPFileDelete.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="Server") String server,
			@InputParameter(name="PortNumber") String portNumber,
			@InputParameter(name="UserName") String user,
			@InputParameter(name="Password") String password,
			@InputParameter(name="FileToDelete", constraints= {FILE, EXISTS}) String fileToDelete
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			) throws Exception {

		int port = Integer.parseInt(portNumber);
		FTPClient ftpClient = new FTPClient();
		try {

			ftpClient.connect(server, port);

			int replyCode = ftpClient.getReplyCode();
			if (!FTPReply.isPositiveCompletion(replyCode)) {
				log.info("Connect failed");
				return new Status("10","Connect failed");
			}

			boolean success = ftpClient.login(user, password);

			if (!success) {
				log.info("Could not login to the server");
				return new Status("11","login failed");
			}

			boolean deleted = ftpClient.deleteFile(fileToDelete);
			if (deleted) {
				log.info("The file was deleted successfully.");
				
			} else {
				log.info("Could not delete the  file, it may not exist.");
			}
			return new Status("00","The file was deleted successfully");
		} catch (IOException e) {
			log.info("Oh no, there was an error: " + e.getMessage());
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);

		} finally {
			// logs out and disconnects from server
			try {
				if (ftpClient.isConnected()) {
					ftpClient.logout();
					ftpClient.disconnect();
				}
			} catch (IOException e) {				
				String className = this.getClass().getSimpleName();
				log.error("Display Error code ::" + className);
	
			}
		}
	

	}
}
