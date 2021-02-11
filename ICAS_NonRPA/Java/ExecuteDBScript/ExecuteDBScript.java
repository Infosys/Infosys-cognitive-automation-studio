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
public class ExecuteDBScript {

	private static final Logger log = LoggerFactory.getLogger(ExecuteDBScript.class);

	public Status execute(
			@InputParameter(name = "ApplicationName") String appName,
			@InputParameter(name = "ApplicationVersion") String appVersion,
			@InputParameter(name = "DBTechnology") String dbTechnology, 
			@InputParameter(name = "URL") String hostName,
			@InputParameter(name = "Configuration") Properties conf
//			@OutputParameter(name="Configuration") ObjectHolder<List<String>> files		  
	) throws Exception {

		try {
			RunSQL(conf, hostName, appName, appVersion, dbTechnology);
			  log.info("process Successfull");
			  return new Status("00","process  Successfully ");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}
	}

	private void RunSQL(Properties conf, String hostName, String appName, String appVersion, String dbTechnology) {
		String command;
		String outputfilePath = conf.getProperty("FilePaths.APP_ROOT");
		File workingDir = GetCurrentWorkingDirectory(appName, appVersion, outputfilePath);
		String[] a = hostName.split("=");
		String s = a[1];
		String[] ss = s.split(";");
		String serverName = ss[0];

		File tempfilePath = new File(conf.getProperty("FilePaths.TEMP"));
		File[] listOfFiles = tempfilePath.listFiles();
		if (listOfFiles.length > 0) {
			String artifactFilePath = listOfFiles[0].getPath();

			command = "sqlcmd -S " + serverName + " -i " + artifactFilePath;
//		command = "sqlcmd -S " +serverName+ " -i C:\\Users\\abhijit_shekhar\\Documents\\botscript.sql";	 
//		command = "sqlcmd -S MYSHEC126753L -i C:\\Users\\abhijit_shekhar\\Documents\\botscript.sql";	
			ExecuteCommand(workingDir, command);
		}
	}

	private static File GetCurrentWorkingDirectory(String appName, String appVersion, String outputfilePath) {
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');
		appName1 = outputfilePath + appName1;
//		appName1 = "D:\\Code\\outputfolder\\ApplicationCode\\" + appName1;
		File workingdir = new File(appName1);
		return workingdir;
//		return  appName1;
	}

	private static void ExecuteCommand(File workingDir, String command) {
		try {
			ProcessBuilder pb = new ProcessBuilder(command.split(" ")).directory(workingDir);
			pb.redirectError(Redirect.INHERIT);
			pb.redirectOutput(Redirect.INHERIT);
			pb.redirectInput(Redirect.INHERIT);
			Process p = pb.start();
			p.waitFor();
		} catch (Exception e) {
			log.error("Error while running the process", e);
//			 throw e;
		}

	}

}
