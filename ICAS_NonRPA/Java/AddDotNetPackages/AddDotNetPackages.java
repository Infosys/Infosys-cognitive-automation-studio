/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.dotnet;

import java.io.File;
import java.lang.ProcessBuilder.Redirect;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;


/**
 * Microbot that generates a JHipster application
 */
public class AddDotNetPackages  {
 
	private static final Logger log = LoggerFactory.getLogger(AddDotNetPackages.class);

  
  public Status execute(

	@InputParameter(name="ApplicationName") String appName,
	@InputParameter(name="ApplicationVersion") String appVersion,
	@InputParameter(name="DBTechnology") String dbTechnology,
	@InputParameter(name="Configuration") Properties conf
//	@OutputParameter(name="files") ObjectHolder<List<String>> files
  ) throws Exception {	 
	   
	try {
		AddPackagetoSolution(conf,appName,appVersion,dbTechnology);
		log.info("AddPackage Successfull");
		return new Status("00","AddPackage  Successfully ");
	} catch (Exception e) {
		return new Status("Error",e.getMessage(),e);
	}
  }

private void AddPackagetoSolution(Properties conf,String appName,String appVersion,String dbTechnology)
{
	String command;
	String outputfilePath = conf.getProperty("FilePaths.APP_ROOT");
	File workingDir = GetCurrentWorkingDirectory(appName,appVersion,outputfilePath);
	command = "dotnet add package Microsoft.EntityFrameworkCore.SqlServer -n";	
	ExecuteCommand(workingDir,command);
	command = "dotnet add package Microsoft.EntityFrameworkCore.Tools -n";	
	ExecuteCommand(workingDir,command);
	command = "dotnet add package Microsoft.EntityFrameworkCore.SqlServer.Design -n";
	ExecuteCommand(workingDir,command);
	command = "dotnet add package Microsoft.VisualStudio.Web.CodeGeneration.Tools -n";
	ExecuteCommand(workingDir,command);
	command = "dotnet add package Microsoft.VisualStudio.Web.CodeGeneration.Design -n";
	ExecuteCommand(workingDir,command);
	command = "dotnet add package Microsoft.EntityFrameworkCore -n";
	ExecuteCommand(workingDir,command);

	
}

private static File GetCurrentWorkingDirectory(String appName, String appVersion,String outputfilePath)
{	
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');
		appName1 = outputfilePath + appName1;
		File workingdir = new File(appName1);
		return workingdir;
		//return  appName1;
}

private static void ExecuteCommand(File workingDir, String command)
{
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
  

}
