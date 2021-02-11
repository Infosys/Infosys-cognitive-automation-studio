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
public class GenerateViewController {

	private static final Logger log = LoggerFactory.getLogger(GenerateViewController.class);

	public Status execute(
			@InputParameter(name = "ApplicationName") String appName,
			@InputParameter(name = "ApplicationVersion") String appVersion,
			@InputParameter(name = "DBTechnology") String dbTechnology,
			@InputParameter(name = "Configuration") Properties conf
			) throws Exception {

			try {
				ScaffoldModel(appName, appVersion, dbTechnology, conf);
				log.info("process Successfull");
				return new Status("00","process  Successfully ");
			} catch (Exception e) {
				return new Status("Error",e.getMessage(),e);
			}
	}

	private void ScaffoldModel(String appName, String appVersion, String dbTechnology, Properties conf)
	
	{
		String command;
		String modelName;
		String outputfilePath = conf.getProperty("FilePaths.APP_ROOT");
		File workingDir = GetCurrentWorkingDirectory(appName, appVersion, outputfilePath);
		String projectname = GetProjectName(appName, appVersion);

		File folder = new File(workingDir.getPath() + "\\Models");
		File[] listOfFiles = folder.listFiles();

		for (int i = 0; i < listOfFiles.length; i++) {
			modelName = listOfFiles[i].getName();
			if (!(modelName.contains("ErrorViewModel.cs") || modelName.contains("Context.cs"))) {
				modelName = modelName.substring(0, modelName.length() - 3);
				command = "";
				command = "dotnet aspnet-codegenerator --project " + workingDir.getPath();
				command = command + " controller --force --controllerName " + modelName + "Controller --model ";
				command = command + projectname + ".Models." + modelName + " --dataContext " + projectname
						+ ".Models.DeveloperBotContext --relativeFolderPath Controllers ";
				command = command + "--controllerNamespace " + projectname + ".Controllers --no-build";
				System.out.println(command);
				ExecuteCommand(workingDir, command);
			}
		}
	}

	private static File GetCurrentWorkingDirectory(String appName, String appVersion, String outputfilePath) {
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');
		appName1 = outputfilePath + appName1;
		// appName1 = "D:\\Code\\outputfolder\\ApplicationCode\\" + appName1;
		File workingdir = new File(appName1);
		return workingdir;
		// return appName1;
	}

	private static String GetProjectName(String appName, String appVersion) {
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');
		return appName1;
		// return appName1;
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
			// throw e;
		}

	}

}
