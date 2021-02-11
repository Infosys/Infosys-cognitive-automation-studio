/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;



import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
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

import com.profesorfalken.jpowershell.PowerShell;
import com.profesorfalken.jpowershell.PowerShellResponse;

@Bot(name = "CheckFileExistsOnWindows", version = "1.0", description = "", botCategory = "String", author = "", technology = "", technologyCode = "01", botCategoryCode = "01", botId = "07")

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

public class CheckFileExistsOnWindows {
	private static final Logger log = LoggerFactory.getLogger(CheckFileExistsOnWindows.class);
	private static final String secretKey = "0025d398c2a01ec9f0510925111797f3187742d34d2e661952deaac8db7196fda018d3adc50daf3cd9ef7b65c22827037c0b";

	@Errors(exceptions = {
			@Error(errorCode = "01010711FF", errorMessagePattern = ".*", exceptionClass = IOException.class) })

	public Status execute(

			@InputParameter(name = "Target") String target, @InputParameter(name = "FileName") String fileName,
			@InputParameter(name = "ServerObject") Server serverObject,
			@OutputParameter(name = "Response") ObjectHolder<String> response

	) throws ExecutionError, IOException {
		String userName = serverObject.getUserName();
		String password = AES.decrypt(serverObject.getPassword(), secretKey).toString();
		String serverName = serverObject.getServerName();
		
		String TargetPath = target + "\\" + fileName;
		String creds ="$Username = '" + userName + "';$HostName='" + serverName + "';$PlainPassword ='" + password
			+"';$SecurePassword = ConvertTo-SecureString -String $PlainPassword -AsPlainText -Force;"
	        +"$mycred = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $Username, $SecurePassword;"
	        +"$session = New-PSSession -ComputerName $($HostName) -Credential $mycred;"
	     	+"$Test=Invoke-Command -Session $Session -ScriptBlock { Test-Path $args[0] } -ArgumentList \""
	        +TargetPath+"\""
	        +";If ($Test) {Write-Host \"True\"}Else {Write-Host \"False\"}";
		log.info("Check File Details...." + TargetPath);
		PowerShell powerShell = null;
		try {
			// Creates PowerShell session
			powerShell = PowerShell.openSession();
			// Increase timeout to give enough time to the script to finish
			Map<String, String> config = new HashMap<String, String>();
			config.put("maxWait", "10000");
			PowerShellResponse responseOutput = powerShell.configuration(config).executeCommand(creds);
			if (responseOutput.isError()) {
				response.setValue("False");
				log.info(responseOutput.getCommandOutput());
				log.info("Internal PowerShell Error");
				powerShell.close();
				return new Status("00", "File not found");
			} else {
				String ReturnValue = responseOutput.getCommandOutput().toString();
				if ("true".equals(ReturnValue.toLowerCase())) {
					response.setValue("True");
					powerShell.close();
					log.info("file found");
					return new Status("00", "File Found Successfully");
				} else {
					response.setValue("False");
					log.info("File not found");
					powerShell.close();
					return new Status("00", "File not found");
				}
			}

		} catch (Exception e) {
			powerShell.close();
			response.setValue("False");
			log.error(e.getMessage());
			return new Status("Error", e.getMessage(), e);
		}

	}

}
