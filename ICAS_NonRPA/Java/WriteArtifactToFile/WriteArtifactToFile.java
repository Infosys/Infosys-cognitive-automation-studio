/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.lang.reflect.Method;
import java.util.List;
import java.util.Properties;
import java.util.Set;
import java.util.TreeMap;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.camunda.bpm.engine.variable.value.ObjectValue;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

//import com.infosys.impact.devbot.custom.AppGenerator;
import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.domain.Artifact;
import com.infosys.impact.botfactory.domain.enumeration.ArtifactType;

public class WriteArtifactToFile implements JavaDelegate {
	private static final Logger log = LoggerFactory.getLogger(WriteArtifactToFile.class);

	public void execute(DelegateExecution execution) throws Exception {
		  logContext(execution);		  
		  String appName = (String) execution.getVariable("ApplicationName");
		  String appVersion = (String) execution.getVariable("ApplicationVersion");
		  Properties conf = (Properties) execution.getVariable("Configuration");
		  TreeMap tm = (TreeMap) execution.getVariable("Params");		  		  
		  //Set<Artifact> artifacts = (java.util.LinkedHashSet<Artifact>) tm.get("Artifacts");
		  Artifact artifact = (Artifact) execution.getVariable("Artifact"); 
		  String searchKey = (String) tm.get("SearchKey");
		  String searchValue = (String) tm.get("SearchValue");
		  String location = (String) tm.get("Location");
		  log.info("************\n\n   artifact = "+artifact+", searchKey = "+searchKey+", searchValue = "+searchValue);
		  if(searchValue==null) {
			  searchValue="";
		  }
		  Class<Artifact> clz= Artifact.class;
		  Method m = clz.getMethod("get"+searchKey.toUpperCase().charAt(0)+searchKey.substring(1));
		  
		  //for(Artifact artifact:artifacts) {
			 //log.info("artifact ="+artifact);
			  //if(searchValue.equals(m.invoke(artifact).toString())){
				//  log.info("found match");  
				  String fileName = artifact.getFileName();
				  if(artifact.getArtifactType().equals(ArtifactType.CODE_SNIPPET)) {
					  fileName=artifact.getId()+".snippet";
				  }
				  byte[] content = artifact.getContent();
				  File wd = Utility.getActualLocation(conf, location, appName);
						  //Utility.createProjectWorkingDirectory(appName, appVersion);
				  Utility.writeFile(new File(wd,fileName).getPath(), content);
			  //}
		  //}		  
	 }
	  protected void logContext(DelegateExecution execution) {
		  log.info("************\n\n   WriteArtifactToFile invoked by "
		            + "processDefinitionId=" + execution.getProcessDefinitionId()
		            + ", activtyId=" + execution.getCurrentActivityId()
		            + ", activtyName='" + execution.getCurrentActivityName() + "'"
		            + ", processInstanceId=" + execution.getProcessInstanceId()
		            + ", businessKey=" + execution.getProcessBusinessKey()
		            + ", executionId=" + execution.getId()
		            + ", var=" + execution.getVariables()
		            + " \n\n***********");
	  }
	  private void generateJHipsterApplication(String appName,String appVersion,String dbTechnology) throws IOException {
			// this.logsService.addLog(generationId, "Running JHipster");
			log.debug("Start:REST request to generate Application Code");
			//change the userID 
			String jhipsterCommand = "C:\\Users\\alok_chand\\AppData\\Roaming\\npm\\jhipster.cmd";
			File workingDir = createProjectWorkingDirectory(appName,appVersion);
			String content = readFile("D:\\Code\\outputfolder\\AppCode2\\.yo-rc.json");
			content = content.replaceAll("\\$AppName", appName);
			//the DB is not taken automatically so it is hardcoded
//			content = content.replaceAll("\\$databaseType",dbTechnology.toLowerCase());
			
			content = content.replaceAll("\\$databaseType","mongoDB");
			// TODO Add package and other params
			writeFile(new File(workingDir, ".yo-rc.json").getPath(), content);

			runProcess(appName, workingDir,
					jhipsterCommand + " --force-insight --skip-checks " + "--skip-install --skip-cache --skip-git");
			// this.runProcess(app.getApplicationName(), workingDir, jhipsterCommand );

			log.debug("End:REST request to generate Application Code");
		}
	  private static String readFile(String path) throws IOException {
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
