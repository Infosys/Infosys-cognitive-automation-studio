/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.java;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

/**
 * Microbot that generates a JHipster application
 */
public class JHipsterApplicationCreationBot {

	private static final Logger log = LoggerFactory.getLogger(JHipsterApplicationCreationBot.class);
	static int portNumber = 1000;

	public Status execute(@InputParameter(name = "Configuration") Properties conf,
			@InputParameter(name = "ApplicationName") String appName,
			@InputParameter(name = "ApplicationVersion") String appVersion,
			@InputParameter(name = "DBTechnology") String dbTechnology,
			@InputParameter(name = "TargetPath") String targetPath,
			@OutputParameter(name = "TablesName") ObjectHolder<String> tableNameOut

	) throws Exception {

		try {
			portNumber++;
			String port = "" + portNumber;
			generateJHipsterApplication(conf, appName, appVersion, dbTechnology, port);
			return new Status("00","Created successfully ");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}

	}

	private void generateJHipsterApplication(Properties conf, String appName, String appVersion, String dbTechnology,
			String portNumber) throws IOException {

		log.debug("Start:REST request to generate Application Code");

		String jhipsterCommand = conf.getProperty("Commands.JHIPSTER");

		File workingDir = createProjectWorkingDirectory(appName, appVersion);

		String content = readFile(conf.getProperty("Templates.YO_RC_JSON"));
		content = content.replaceAll("\\$AppName", appName);
		content = content.replaceAll("\\$databaseType", "mongodb");

		content = content.replaceAll("\\$portNumber", portNumber);
		log.info("This is the port number " + portNumber);

		writeFile(new File(workingDir, ".yo-rc.json").getPath(), content);

		runProcess(appName, workingDir,
				jhipsterCommand + " --force-insight --skip-checks " + "--skip-install --skip-cache --skip-git");


		log.debug("End:REST request to generate Application Code");
	}

	private static String readFile(String path) throws IOException {
		System.out.println(path);
		BufferedReader reader = new BufferedReader(new FileReader(path));
		StringBuffer sb = new StringBuffer();
		String l = null;
		do {
			l = reader.readLine();
			if (l != null) {
				sb.append(l + "\n");
			}
		} while (l != null);
		reader.close();
		return sb.toString();
	}

	private static void writeFile(String path, String content) throws IOException {
		FileWriter wr = new FileWriter(path);
		wr.write(content);
		wr.close();
	}

	private static File createProjectWorkingDirectory(String appName, String appVersion) {
		String appName1 = appName + "_" + appVersion;
		appName1 = appName1.replace('.', '_');
		appName1 = appName1.replace('/', '_');
		appName1 = appName1.replace('\\', '_');
		appName1 = appName1.replace(' ', '_');
		File workingDir = new File("D:\\Code\\outputfolder\\ApplicationCode\\" + appName1);

		workingDir.mkdirs();

		return workingDir;
	}

	public static void runProcess(String generationId, File workingDir, String command) {
		log.info("Running command: \"{}\" in directory:  \"{}\"", command, workingDir);

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
