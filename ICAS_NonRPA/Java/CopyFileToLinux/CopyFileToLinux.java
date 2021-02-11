/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.custom.AES;
import com.infosys.impact.botfactory.domain.Server;
import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpATTRS;
import com.jcraft.jsch.UserInfo;

@Bot(name = "CopyFileToLinux", version = "1.0", description = "", botCategory = "String", author = "",
	technology = "", technologyCode = "01", botCategoryCode = "01", botId = "09")

//ErrorCategory(ValidationError: 1, ConnectionError: 2,AccessError : 3, DiskIOError: 4, DBIOError: 5,
//               NetworkIOError: 6, ConfigurationError: 7)
//botCode = technologyCode + categoryCode + botId
//botErrorCode = errorCategoryCode + errorCodeA + errorCodeB
//errorCode = botCode + botErrorCode  
//
//String botErrorCode;
//String errorCategoryCode;
//String errorCodeA = "1";
//String errorCodeB;
//String errorDescrption;

public class CopyFileToLinux {
	private static final Logger log = LoggerFactory.getLogger(CopyFileToLinux.class);
	private static final String secretKey = "0025d398c2a01ec9f0510925111797f3187742d34d2e661952deaac8db7196fda018d3adc50daf3cd9ef7b65c22827037c0b";

	@Errors(exceptions = {
			@Error(errorCode = "01010911FF", errorMessagePattern = ".*", exceptionClass = IOException.class) })

	public Status execute(
			@InputParameter(name = "Source", constraints = { EXISTS }) String source,
			@InputParameter(name = "Target") String target,
			@InputParameter(name = "FileName") String fileName,
			@InputParameter(name="ServerObject") Server serverObject,
			@OutputParameter(name="Response") ObjectHolder<String> response
			
	) throws ExecutionError, IOException {
        String userName=serverObject.getUserName();
		String password = AES.decrypt(serverObject.getPassword(), secretKey).toString();
		String host=serverObject.getServerName();
		String SourcePath = source+"\\"+fileName;
		String TargetPath = "/"+target+"/"+fileName;
		
		log.info("Copy File Details...." + SourcePath);

		try {
			JSch jsch = new JSch();
			/*
			 *  Open a new session, with your username, host and port Set the password and
			 * call connect. session.connect() opens a new connection to remote SSH server.
			 * Once the connection is established, you can initiate a new channel. this
			 * channel is needed to connect to remotely execution program
			 */
			Session session = jsch.getSession(userName, host, 22);
			session.setConfig("StrictHostKeyChecking", "no");
			session.setPassword(password);
			session.connect();
			ChannelSftp channelSftp = (ChannelSftp) session.openChannel( "sftp" );
		    channelSftp.connect();
		    log.info("SFTP Connected Successfull");
			channelSftp.put(SourcePath,TargetPath);
			response.setValue("True");
			log.info("Copy Successfull");
			channelSftp.exit();
			return new Status("00",	"Copied file Successfully");
			
		}   catch (Exception e) {
			log.error(e.getMessage());
			response.setValue("False");
			return new Status("Error",e.getMessage(),e);
		}

	}
	

}
