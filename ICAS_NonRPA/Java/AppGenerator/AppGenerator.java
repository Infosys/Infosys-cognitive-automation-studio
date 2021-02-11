/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.devbot.custom;

import com.infosys.impact.devbot.domain.Application;
import com.infosys.impact.devbot.domain.Artifact;
import com.infosys.impact.devbot.repository.ApplicationRepository;
import com.infosys.impact.devbot.repository.ArtifactRepository;
import com.infosys.impact.devbot.repository.AssetRepository;
import com.infosys.impact.devbot.web.rest.errors.BadRequestAlertException;
import com.infosys.impact.devbot.web.rest.util.HeaderUtil;
import io.github.jhipster.web.util.ResponseUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Example;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.net.URI;
import java.net.URISyntaxException;

import java.lang.ProcessBuilder.Redirect;

import java.util.List;
import java.util.Optional;

@Component
public class AppGenerator {
	
	public AppGenerator(AssetRepository assetRepository,ArtifactRepository artifactRepository) {
		this.assetRepository = assetRepository;
		this.artifactRepository = artifactRepository;
	}

	
	

    private AssetRepository assetRepository;
	
	private ArtifactRepository artifactRepository;
	
	private final Logger log = LoggerFactory.getLogger(AppGenerator.class);

	public void generateApplicationCode(Application app) throws IOException {
		String techStackName = app.getTechnologyStack().getTechnologyStackUniqueName();
		String templateName = app.getTemplate().getName();
		if(templateName != "")
		{
			generateCodefromTemplate(app);
		}
		else
		{
			if ("Angular7-Springboot-MongoDB".equals(techStackName)) {
				generateJHipsterApplication(app);
			} else if ("Angular7-DotNetMVC-MSSQLServer".equals(techStackName)) {
				generateDotNetNewApplication(app);
			} else {
				log.error("Unsupported technology stack {}",techStackName );
			}			
		}
	}

	public void runProcess(String generationId, File workingDir, String command) {
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

	private String readFile(String path) throws IOException {
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

	private void writeFile(String path, String content) throws IOException {
		FileWriter wr = new FileWriter(path);
		wr.write(content);
		wr.close();
	}

	private File createProjectWorkingDirectory(Application app) {
		String appName = app.getApplicationName() + "_" + app.getApplicationVersion();
		appName = appName.replace('.', '_');
		appName = appName.replace('/', '_');
		appName = appName.replace('\\', '_');
		appName = appName.replace(' ', '_');
		File workingDir = new File("D:\\Code\\outputfolder\\ApplicationCode\\" + appName);
		workingDir.mkdirs();
		return workingDir;
	}

	private void generateJHipsterApplication(Application app) throws IOException {
		// this.logsService.addLog(generationId, "Running JHipster");
		log.debug("Start:REST request to generate Application Code");
		String jhipsterCommand = "C:\\Users\\Rajagopal_Neralla\\AppData\\Roaming\\npm\\jhipster.cmd";
		File workingDir = createProjectWorkingDirectory(app);
		String content = readFile("D:\\Code\\outputfolder\\AppCode2\\.yo-rc.json");
		content = content.replaceAll("\\$AppName", app.getApplicationName());
		content = content.replaceAll("\\$databaseType",
				app.getDbTechnology().getTechnology().getTechnologyName().toLowerCase());
		// TODO Add package and other params
		writeFile(new File(workingDir, ".yo-rc.json").getPath(), content);

		runProcess(app.getApplicationName(), workingDir,
				jhipsterCommand + " --force-insight --skip-checks " + "--skip-install --skip-cache --skip-git");
		// this.runProcess(app.getApplicationName(), workingDir, jhipsterCommand );

		log.debug("End:REST request to generate Application Code");
	}

	private void generateDotNetNewApplication(Application app) {
		String command;
		command = "\"C:\\Program Files\\dotnet\\dotnet.exe\" new angular -o \""+app.getApplicationName()+"\"";
		File workingDir = createProjectWorkingDirectory(app);
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
	
	private void generateCodefromTemplate(Application app) throws IOException {
		// this.logsService.addLog(generationId, "Running JHipster");
		log.debug("Start:REST request to generate Application Code from Template");
		File workingDir = createProjectWorkingDirectory(app);
		String templateName = app.getTemplate().getName();
		//Code to read file content tes
		//String content = app.
		//TODO assetRepository.findAll("")
		log.debug(" {} Template name",templateName);
		Artifact sampleartifact = new Artifact();
		sampleartifact.setArtifactName(templateName);
		List<Artifact> ar = artifactRepository.findAll(Example.of(sampleartifact));
		//List<Artifact> ar = artifactRepository.
		 if(ar.size()==0) {
			 log.debug("No templates available for code generation");
		 }
		 else
		 {
			 log.debug("{} template pending for code generation",ar.size());
			 for(Artifact a:ar) {
		        	log.info("Code Generation from template {}  queued",a.getArtifactName());  
		        	writeFile(new File(workingDir,templateName).getPath(), new String(a.getContent()));
		        	     	
		        }
		 }

		log.debug("End:REST request to generate Application Code");
	}
}