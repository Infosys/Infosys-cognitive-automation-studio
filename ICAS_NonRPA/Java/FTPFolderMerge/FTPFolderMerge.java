/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.ftp;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import org.apache.commons.net.ftp.FTP;
import org.apache.commons.net.ftp.FTPClient;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FTPFolderMerge {

	private static final Logger log = LoggerFactory.getLogger(FTPFolderMerge.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="Server") String server,
			@InputParameter(name="PortNumber") String portNumber,
			@InputParameter(name="UserName") String user,
			@InputParameter(name="Password") String password,
			@InputParameter(name="ToMergeFolderFrom", constraints= {FOLDER, EXISTS}) String folderFrom,
			@InputParameter(name="FolderTo", constraints= {FOLDER, EXISTS}) String folderTo
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files	
			) throws Exception {

		int port = Integer.parseInt(portNumber);
		FTPClient ftpClient = new FTPClient();

		try {

			ftpClient.connect(server, port);
			ftpClient.login(user, password);
			ftpClient.enterLocalPassiveMode();

			log.info("Connected");

			uploadDirectory(ftpClient, folderTo, folderFrom, "");

			ftpClient.logout();
			ftpClient.disconnect();

			log.info("Disconnected");
			return new Status("00","Process Sucessfull");
		} catch (IOException e) {
			e.printStackTrace();
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}

	}

	public static void uploadDirectory(FTPClient ftpClient, String remoteDirPath, String localParentDir,
			String remoteParentDir) throws IOException {

		log.info("LISTING directory: " + localParentDir);

		File localDir = new File(localParentDir);
		File[] subFiles = localDir.listFiles();
		if (subFiles != null && subFiles.length > 0) {
			for (File item : subFiles) {
				String remoteFilePath = remoteDirPath + "/" + remoteParentDir + "/" + item.getName();
				if (remoteParentDir.equals("")) {
					remoteFilePath = remoteDirPath + "/" + item.getName();
				}

				if (item.isFile()) {
					// upload the file
					String localFilePath = item.getAbsolutePath();
					log.info("About to upload the file: " + localFilePath);
					boolean uploaded = uploadSingleFile(ftpClient, localFilePath, remoteFilePath);
					if (uploaded) {
						log.info("UPLOADED a file to: " + remoteFilePath);
					} else {
						log.info("COULD NOT upload the file: " + localFilePath);
					}
				} else {
					// create directory on the server
					boolean created = ftpClient.makeDirectory(remoteFilePath);
					if (created) {
						log.info("CREATED the directory: " + remoteFilePath);
					} else {
						log.info("COULD NOT create the directory: " + remoteFilePath);
					}

					// upload the sub directory
					String parent = remoteParentDir + "/" + item.getName();
					if (remoteParentDir.equals("")) {
						parent = item.getName();
					}

					localParentDir = item.getAbsolutePath();
					uploadDirectory(ftpClient, remoteDirPath, localParentDir, parent);
				}
			}
		}
	}

	public static boolean uploadSingleFile(FTPClient ftpClient, String localFilePath, String remoteFilePath)
			throws IOException {
		File localFile = new File(localFilePath);

		InputStream inputStream = new FileInputStream(localFile);
		try {
			ftpClient.setFileType(FTP.BINARY_FILE_TYPE);
			return ftpClient.storeFile(remoteFilePath, inputStream);
		} finally {
			inputStream.close();
		}
	}
}
