/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.dotnet;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Properties;
import java.util.Scanner;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

/**
 * Microbot that generates a JHipster application
 */
public class CodeInjector {
 
	private static final Logger log = LoggerFactory.getLogger(CodeInjector.class);

  
  public Status execute(
	@InputParameter(name="ApplicationName") String appName,
	@InputParameter(name="ApplicationVersion") String appVersion,
	@InputParameter(name="DBTechnology") String dbTechnology,
	@InputParameter(name="Configuration") Properties conf,
	@InputParameter(name="URL") String dbConnectionString
//	@OutputParameter(name="Configuration") ObjectHolder<List<String>> files

  ) throws Exception {
	  
	  try {
		InjectCodeforStart(dbConnectionString,appName,appVersion,dbTechnology,conf);
		  log.info("process Successfull");
		  return new Status("00","process  Successfully ");
	} catch (Exception e) {
		return new Status("Error",e.getMessage(),e);
	}
  }
    

private void InjectCodeforStart(String dbConnectionString,String appName,String appVersion,String dbTechnology,Properties conf)
{	
	String outputfilePath = conf.getProperty("FilePaths.APP_ROOT");
	File workingDir = GetCurrentWorkingDirectory(appName, appVersion, outputfilePath);
	String projectname =  GetProjectName(appName,appVersion);
	String startupFilePath = workingDir.getPath();
	String matchText = "using Microsoft.Extensions.DependencyInjection;";
	String appendText = "using " + projectname + ".Models;\nusing Microsoft.EntityFrameworkCore;\n";
	AppendCode(startupFilePath,matchText,appendText);
	matchText = "services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_2);";
	//appendText ="var connection = @\"Server=MYSHEC126753L;Database=DeveloperBot;Trusted_Connection=True;\";\nservices.AddDbContext<DeveloperBotContext>(options => options.UseSqlServer(connection));\n";
	appendText ="var connection = @\""+dbConnectionString+"Trusted_Connection=True;\";\nservices.AddDbContext<DeveloperBotContext>(options => options.UseSqlServer(connection));\n"; 
	AppendCode(startupFilePath,matchText,appendText);
}

private static File GetCurrentWorkingDirectory(String appName, String appVersion,String outputfilePath)
{	
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');
		appName1 = outputfilePath + appName1 + "\\Startup.cs";
		//appName1 = "D:\\Code\\outputfolder\\ApplicationCode\\" + appName1 + "\\Startup.cs";
		
		File workingdir = new File(appName1);
		return workingdir;
		//return  appName1;
}

private static String GetProjectName(String appName, String appVersion)
{	
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');		
		return appName1;
		//return  appName1;
}

private static void AppendCode(String filePath, String matchText, String appendText)
{		
	try
	{
	
	File input = new File(filePath);	
	Scanner sc = new Scanner(input);   
	
	String app ="";
	while(sc.hasNextLine()) {
		
		String s = sc.nextLine();
		app += s+"\n";		
		
		//System.out.println("each line="+s);
		if( (s != null) && s.trim().equals(matchText) )
		{
			app += appendText;
		}
	}
	File output = new File(filePath);
	PrintWriter printer = new PrintWriter(output);
	
	printer.write(app+"\n");
	printer.flush();
	printer.close();	
	sc.close();
}
catch(FileNotFoundException e) {
	log.error("File not found. Please scan in new file.");
}

}
  

}
