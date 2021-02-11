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
import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FTPFileRename {

	private static final Logger log = LoggerFactory.getLogger(FTPFileRename.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(			
			@InputParameter(name="Server") String server,
			@InputParameter(name="PortNumber") String portNumber,
			@InputParameter(name="UserName") String user,
			@InputParameter(name="Password") String password,
			@InputParameter(name="OldFilePath", constraints= {FILE, EXISTS}) String oldFile,
			@InputParameter(name="NewFilePath") String newFile
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			) throws Exception {				

        int port =  Integer.parseInt(portNumber);
        
        FTPClient ftpClient = new FTPClient();
        try {
            ftpClient.connect(server, port);
            ftpClient.login(user, password);     
 
            boolean success = ftpClient.rename(oldFile, newFile);
            if (success) {
                log.info(oldFile + " was successfully renamed to: "
                        + newFile);
            } else {
                log.info("Failed to rename: " + oldFile);
            }
            return new Status("00","file renamed successfully");
            
        } catch (IOException e) {

			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);

        } finally {
            if (ftpClient.isConnected()) {
                try {
                    ftpClient.logout();
                    ftpClient.disconnect();
                } catch (IOException e) {
        			String className = this.getClass().getSimpleName();
        			log.info("Display Error code ::" + className);

                }
            }
        }
        
	}
}
