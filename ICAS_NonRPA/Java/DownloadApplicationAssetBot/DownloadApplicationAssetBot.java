/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.devbot.microbots;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.util.List;
import java.util.Optional;
import java.util.Set;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.camunda.bpm.engine.variable.value.ObjectValue;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Example;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.devbot.custom.AppGenerationJob;
import com.infosys.impact.devbot.custom.AppGenerator;
import com.infosys.impact.devbot.custom.ArchiveUtility;
import com.infosys.impact.devbot.custom.Utility;
import com.infosys.impact.devbot.domain.Application;
import com.infosys.impact.devbot.domain.ApplicationComponent;
import com.infosys.impact.devbot.domain.Artifact;
import com.infosys.impact.devbot.domain.Asset;
import com.infosys.impact.devbot.domain.enumeration.ArtifactType;
import com.infosys.impact.devbot.repository.ApplicationRepository;
import com.infosys.impact.devbot.repository.AssetRepository;
import com.infosys.impact.devbot.repository.TechnologyRepository;

/**
 * Microbot that generates a JHipster application
 */
@RestController
@RequestMapping("/api")
public class DownloadApplicationAssetBot {

	private static final Logger log = LoggerFactory.getLogger(AppGenerator.class);
	@Autowired
	private ApplicationRepository applicationRepository;

	@Autowired
	private TechnologyRepository technologyRepository;

	@Autowired
	private AssetRepository assetRepository;
	//FIXME Needs to be replaced with POST method as this changes the state of the system.
	@GetMapping("/download/{appId}/{compId}")
	public void execute(@PathVariable String appId,@PathVariable String compId) throws Exception {
		/*
		 * Application sample = new Application();
		 * sample.setCodeGenerationStatus("TBD"); sample.setComponents(null);
		 * sample.setOthers(null);
		 */
		Optional<Application> oapp = applicationRepository.findById(appId);
		if (oapp.equals(Optional.empty())) {
			log.info("App does not exists");
			return;
		}
		Application app = oapp.get();
		
		if (app.getTemplate() == null) {
			log.info("App does not have an associated template");
			return;
		}
		File workingDir = createProjectWorkingDirectory(app.getApplicationName(),
				app.getApplicationVersion());
		if(compId.equals("app")) {
			log.info("Downloading Application Template content");
			downloadTemplate(app.getTemplate().getName(),workingDir);
		}else {
			log.info("Downloading Template content for component "+compId);
			for(ApplicationComponent ac:app.getComponents()) {
				if(ac.getId().equals(compId)) {
					log.info("Found component "+compId);
					downloadTemplate(ac.getAsset().getAssetName(),workingDir);
				}
			}
		}
	}
	private void downloadTemplate(String assetName,File workingDir) throws IOException {
		Asset sample = new Asset();
		sample.setAssetName(assetName);
		sample.setArtifacts(null);
		Optional<Asset> asset = assetRepository.findOne(Example.of(sample));
		if (!asset.equals(Optional.empty())) {
			Set<Artifact> s = asset.get().getArtifacts();
			for (Artifact a : s) {
				if (ArtifactType.SOURCE_CODE.equals(a.getArtifactType())) {
					byte[] content = a.getContent();					
					File tempFile = new File(System.getProperty("java.io.tmpdir"), a.getFileName());
					writeFile(tempFile.getPath(), content);
					if (a.getFileName().endsWith(".zip")) {
						ArchiveUtility.extractArchive(tempFile.getPath(), null, workingDir.getPath());
					} else {
						tempFile.renameTo(new File(workingDir, a.getFileName()));
					}
				}
			}
		}
	}

	private static void writeFile(String path, byte[] content) throws IOException {
		FileOutputStream wr = new FileOutputStream(path);
		wr.write(content);
		wr.close();
	}

	private static void writeFile(String path, String content) throws IOException {
		FileWriter wr = new FileWriter(path);
		wr.write(content);
		wr.close();
	}

	protected void logContext(DelegateExecution execution) {
		log.info("************\n\n   LoggerDelegate invoked by " + "processDefinitionId="
				+ execution.getProcessDefinitionId() + ", activtyId=" + execution.getCurrentActivityId()
				+ ", activtyName='" + execution.getCurrentActivityName() + "'" + ", processInstanceId="
				+ execution.getProcessInstanceId() + ", businessKey=" + execution.getProcessBusinessKey()
				+ ", executionId=" + execution.getId() + " \n\n***********");
	}

	private void generateJHipsterApplication(String appName, String appVersion, String dbTechnology)
			throws IOException {
		// this.logsService.addLog(generationId, "Running JHipster");
		log.debug("Start:REST request to generate Application Code");
		String jhipsterCommand = "C:\\Users\\Rajagopal_Neralla\\AppData\\Roaming\\npm\\jhipster.cmd";
		File workingDir = createProjectWorkingDirectory(appName, appVersion);
		String content = readFile("D:\\Code\\outputfolder\\AppCode2\\.yo-rc.json");
		content = content.replaceAll("\\$AppName", appName);
		content = content.replaceAll("\\$databaseType", dbTechnology.toLowerCase());
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
