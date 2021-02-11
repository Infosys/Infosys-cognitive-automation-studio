/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.dotnet;

import java.io.File;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.util.Properties;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

/**
 * Microbot that generates a JHipster application
 */
public class DotNetNewApplicationCreationBot {
 
	private static final Logger log = LoggerFactory.getLogger(DotNetNewApplicationCreationBot.class);

  
  public Status execute(
	@InputParameter(name="ApplicationName") String appName,
	@InputParameter(name="ApplicationVersion") String appVersion,
	@InputParameter(name="DBTechnology") String dbTechnology,
	@InputParameter(name="Configuration") Properties conf
//	@OutputParameter(name="Configuration") ObjectHolder<List<String>> files
	  ) throws Exception {

	  try {
		generateDotNetNewApplication(conf,appName,appVersion,dbTechnology);
		  log.info("process Successfull");
		  return new Status("00","process  Successfully ");
	} catch (Exception e) {
		return new Status("Error",e.getMessage(),e);
	}
  }
  
   private void generateDotNetNewApplication(Properties conf,String appName,String appVersion,String dbTechnology) {
	String command;
	//command = "\"C:\\Program Files\\dotnet\\dotnet.exe\" new mvc -o \""+appName+"\"";
	String dotnetCommand=conf.getProperty("Commands.DOTNET");
	String outputfilePath = conf.getProperty("FilePaths.APP_ROOT");
	File tempfilePath = new File(conf.getProperty("FilePaths.TEMP"));

	if(tempfilePath.exists())
	{
			try {
				FileUtils.cleanDirectory(tempfilePath);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	}
	command = dotnetCommand + " new mvc";
	//command = "\"C:\\Program Files\\dotnet\\dotnet.exe\" new mvc";
	File workingDir = createProjectWorkingDirectory(appName,appVersion,outputfilePath);
	try {
		ProcessBuilder pb = new ProcessBuilder(command.split(" ")).directory(workingDir);
		pb.redirectError(Redirect.INHERIT);
		pb.redirectOutput(Redirect.INHERIT);
		pb.redirectInput(Redirect.INHERIT);
		Process p = pb.start();
		p.waitFor();
	} catch (Exception e) {
		log.error("Error while running the process", e);
		// throw e;
	}
}
private static File createProjectWorkingDirectory(String appName, String appVersion,String outputfilePath) {
	String appName1 = appName + "_" + appVersion;
	appName1 = appName1.replace('.', '_');
	appName1 = appName1.replace('/', '_');
	appName1 = appName1.replace('\\', '_');
	appName1 = appName1.replace(' ', '_');
	// File workingDir = new File("D:\\Code\\outputfolder\\ApplicationCode\\" + appName1);	
		
	File workingDir = new File(outputfilePath + appName1);	
	if(workingDir.exists())
	{
		try {
			FileUtils.deleteDirectory(workingDir);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	workingDir.mkdirs();

	return workingDir;
}


}
