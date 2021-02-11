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
public class GenerateModel {

	private static final Logger log = LoggerFactory.getLogger(GenerateModel.class);

	public Status execute(
			@InputParameter(name = "ApplicationName") String appName,
			@InputParameter(name = "ApplicationVersion") String appVersion,
			@InputParameter(name = "DBTechnology") String dbTechnology,
			@InputParameter(name = "URL") String dbConnectionString,
			@InputParameter(name = "Configuration") Properties conf
//	 @OutputParameter(name="Configuration") ObjectHolder<List<String>> files
	) throws Exception {

		try {
			ScaffoldModel(dbConnectionString, appName, appVersion, dbTechnology, conf);
			return new Status("00","process  Successfully ");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}
	}

	private Status ScaffoldModel(String dbConnection, String appName, String appVersion, String dbTechnology,
			Properties conf) {
		String command;
		String outputfilePath = conf.getProperty("FilePaths.APP_ROOT");
		File workingDir = GetCurrentWorkingDirectory(appName, appVersion, outputfilePath);
		
		command = "dotnet ef dbcontext scaffold \"" + dbConnection
				+ "Trusted_Connection=True;\" Microsoft.EntityFrameworkCore.SqlServer --output-dir Models";
		ExecuteCommand(workingDir, command);
		  log.info("process Successfull");
		  return new Status("00","process  Successfully ");
	}

	private static File GetCurrentWorkingDirectory(String appName, String appVersion, String outputfilePath) {
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');
		appName1 = outputfilePath + appName1;
		File workingdir = new File(appName1);
		
		return workingdir;

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

		}

	}

}
