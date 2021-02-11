/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.ftp;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.apache.commons.net.ftp.FTP;
import org.apache.commons.net.ftp.FTPClient;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FTPFileMove  {

	private static final Logger log = LoggerFactory.getLogger(FTPFileMove.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="Server") String server,
			@InputParameter(name="PortNumber") String portNumber,
			@InputParameter(name="UserName") String user,
			@InputParameter(name="Password") String password,
			@InputParameter(name="FilePath", constraints= {FILE, EXISTS}) String filePath
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			
			) throws Exception {


		int port = Integer.parseInt(portNumber);

		FTPClient ftpClient = new FTPClient();
		try {

			ftpClient.connect(server, port);
			ftpClient.login(user, password);
			ftpClient.enterLocalPassiveMode();

			ftpClient.setFileType(FTP.BINARY_FILE_TYPE);

			File file = new File(filePath);
			if (file.exists()) {

				String[] remoteDir = filePath.split(":", 2);
				String sRemoteFile = remoteDir[1];

				log.info("sRemoteFile is ::" + sRemoteFile);

				File sRemoteFilePath = new File(sRemoteFile);

				if (sRemoteFilePath.exists()) {
					ftpClient.makeDirectory(sRemoteFilePath.getParent());
				} else {
					ftpClient.makeDirectory(sRemoteFilePath.getParent());
				}

				InputStream inputStream = new FileInputStream(file);

				OutputStream outputStream = ftpClient.storeFileStream(sRemoteFile);
				byte[] bytesIn = new byte[4096];
				int read = 0;

				while ((read = inputStream.read(bytesIn)) != -1) {
					outputStream.write(bytesIn, 0, read);
				}
				inputStream.close();
				outputStream.close();

				boolean completed = ftpClient.completePendingCommand();
				if (completed) {
					log.info("Process successfull.");
					file.delete();
				}
			} else {
				log.info(file.getName() + "File is not exist");
			}
			return new Status("00","Process successfull");

		} catch (IOException e) {
			log.info("Error: " + e.getMessage());
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);

		} finally {
			try {
				if (ftpClient.isConnected()) {
					ftpClient.logout();
					ftpClient.disconnect();
				}
			} catch (IOException e) {
				String className = this.getClass().getSimpleName();
				log.info("Display Error code ::" + className);

			}
		}

	}
}