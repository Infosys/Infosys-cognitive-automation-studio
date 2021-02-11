/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.ftp;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.IOException;

import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPFile;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FTPFolderDelete  {

	private static final Logger log = LoggerFactory.getLogger(FTPFolderDelete.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="Server") String server,
			@InputParameter(name="PortNumber") String portNumber,
			@InputParameter(name="UserName") String user,
			@InputParameter(name="Password") String password,
			@InputParameter(name="FolderToDelete", constraints= {FOLDER, EXISTS} ) String folderToDelete
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files			
			) throws Exception {

		int port = Integer.parseInt(portNumber);
		FTPClient ftpClient = new FTPClient();

		try {
			// connect and login to the server
			ftpClient.connect(server, port);
			ftpClient.login(user, password);

			// use local passive mode to pass firewall
			ftpClient.enterLocalPassiveMode();

			log.info("Connected");

			removeDirectory(ftpClient, folderToDelete, "");

			// log out and disconnect from the server
			ftpClient.logout();
			ftpClient.disconnect();

			log.info("Disconnected");
			return new Status("00","Process Sucessfull");
			
		} catch (IOException e) {

			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}

	}

	public void removeDirectory(FTPClient ftpClient, String parentDir, String currentDir) throws IOException {
		String dirToList = parentDir;
		if (!currentDir.equals("")) {
			dirToList += "/" + currentDir;
		}

		FTPFile[] subFiles = ftpClient.listFiles(dirToList);

		if (subFiles != null && subFiles.length > 0) {
			for (FTPFile aFile : subFiles) {
				String currentFileName = aFile.getName();
				if (currentFileName.equals(".") || currentFileName.equals("..")) {
					// skip parent directory and the directory itself
					continue;
				}
				String filePath = parentDir + "/" + currentDir + "/" + currentFileName;
				if (currentDir.equals("")) {
					filePath = parentDir + "/" + currentFileName;
				}

				if (aFile.isDirectory()) {
					// remove the sub directory
					removeDirectory(ftpClient, dirToList, currentFileName);
				} else {
					// delete the file
					boolean deleted = ftpClient.deleteFile(filePath);
					if (deleted) {
						log.info("DELETED the file: " + filePath);
					} else {
						log.info("CANNOT delete the file: " + filePath);
					}
				}
			}

			// finally, remove the directory itself
			boolean removed = ftpClient.removeDirectory(dirToList);
			if (removed) {
				log.info("REMOVED the directory: " + dirToList);
			} else {
				log.info("CANNOT remove the directory: " + dirToList);
			}
		}
	}

}
