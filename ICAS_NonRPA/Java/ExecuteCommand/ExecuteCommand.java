/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.system;


import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;


//*****************************************************
//Bot Name --ExecuteCommand
//Bot Category --System
//Author --IMPACT TEAM
//Bot Description-- To execute Commands
//Describe about the input and output parameters  
//*****************************************************

@Bot(name = "ExecuteCommand", version = "1.0", description = "To execute Commands", botCategory = "System", author = "IMPACT TEAM", technology = "Java",
            technologyCode = "01", botCategoryCode = "01", botId = "01")


public class ExecuteCommand {
	private static final Logger log = LoggerFactory.getLogger(ExecuteCommand.class);
	@Errors(exceptions= {
	
			@Error(errorCode = "01010111FF", errorMessagePattern = ".*", exceptionClass = IOException.class)
		})

	public Status execute(
			@InputParameter(name = "SourcePath", constraints = { EXISTS }) String sourcePath,
			@InputParameter(name = "Command") String command,
			@OutputParameter(name = "Response") ObjectHolder<String> response,
			@OutputParameter(name = "BuildState") ObjectHolder<byte[]> buildState
			) throws Exception , ExecutionError, IOException{		
		
		log.info("Compiling Details...." + sourcePath);
		try {
			 ProcessBuilder builder = new ProcessBuilder("cmd.exe", "/c", "cd \""+sourcePath+"\" && "+command+" && echo Compiled Successfully");
		        builder.redirectErrorStream(true);
		        Process p = builder.start();
		        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
		        String line;
		        String Final="";
		        while (true) {
		            line = r.readLine();
		            if (line == null) { break; }
		            if(line.contains("Compiled Successfully")) { 
		            	buildState.setValue(Final.getBytes());
		            	response.setValue("True");
		            	log.info("Compiled Successfully");
		            	 return new Status("00", "Compiled Successfully");
		            }
		            Final+=line+"\n";
		        }
            	buildState.setValue(Final.getBytes());
		        response.setValue("False");
		        log.info(" Compilation Failed");
		        return new Status("00", "Compilation failed ");
		        
		} catch (Exception e) {
			buildState.setValue(null);
			response.setValue("False");
			log.error(e.getMessage());
			return new Status("Error", e.getMessage(), e);
		}
      

	}

}
