/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.domain.AppRuntime;
import com.infosys.impact.botfactory.domain.Application;
import com.infosys.impact.botfactory.domain.enumeration.RuntimeType;
import com.infosys.impact.botfactory.microbot.file.MoveFolder;
import com.infosys.impact.botfactory.microbot.filemodification.ListFiles;
import com.infosys.impact.botfactory.repository.AppRuntimeRepository;
import com.infosys.impact.botfactory.repository.ApplicationRepository;
import com.infosys.impact.botfactory.repository.ConfigurationEntryRepository;



/**
 * Microbot that a Copy NodeModule & generates JHipster application
 *
 */
@RestController
@RequestMapping("/api")
public class IntrospectFolder { 

	private static final Logger log = LoggerFactory.getLogger(IntrospectFolder.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;
	@Autowired
	private ApplicationRepository applicationRepository;
	@Autowired
	private AppRuntimeRepository appRuntimeRepository;
	
	public IntrospectFolder() {
	}
	

	public IntrospectFolder(ConfigurationEntryRepository configRepository, ApplicationRepository applicationRepository,
			AppRuntimeRepository appRuntimeRepository) {
		super();
		this.configRepository = configRepository;
		this.applicationRepository = applicationRepository;
		this.appRuntimeRepository = appRuntimeRepository;
	}


	@GetMapping({ "/IntrospectFolder" })
	public void execute(@RequestParam Long appId) throws Exception {
		log.info("********** IntrospectFolder *********** "+appId);
		Application app = applicationRepository.findById(appId).get();
		log.info("app ::"+app);
		String folderName = app.getApplicationName() + "_" + app.getApplicationVersion();
		folderName = folderName.replaceAll(" ", "_");
		folderName = folderName.replaceAll("\\.", "_");
		File parent = Utility.getActualLocation(configRepository, "APP_ROOT", folderName);
		//TODO get all runtime with give app name and delete them.
		//app.getRuntimes().clear();
		applicationRepository.save(app);
		checkForNPM(app, parent);
		checkForMaven(app, parent);
		if(parent.listFiles()!=null) {		
			for (File f : parent.listFiles()) {
				if (f.isDirectory()) {
					checkForNPM(app, f);
					checkForMaven(app, f);
				}
			}
		}		
		List<String> files = new ArrayList<>();
		ListFiles.listFiles(parent, files, "Startup.cs");
		
		String[] startUpFiles= files.toArray(new String[] {});
		
		for(String su:startUpFiles) {
			File appFolder = new File(su).getParentFile();
			log.debug("**** app.getApplicationName() is :: " + app.getApplicationName());
			AppRuntime appRuntime = new AppRuntime().name(app.getApplicationName()+"_FE").runtimeType(RuntimeType.FRONT_END)
					.runTimeCommand("DOT_NET_RUN").runtimePort(90001).runTimePath(appFolder.getPath());
			log.debug("**** npm start is appRuntime ::" + appRuntime);
			appRuntimeRepository.save(appRuntime);
			//not required app.addRuntime(appRuntime);
			applicationRepository.save(app);
		}
	}

	private void checkForNPM(Application app, File appFolder) {
		log.info("**** inside npm start **********");
		if (new File(appFolder, "package.json").exists()) {
			log.info("Folder {} contains package.json file.", appFolder.getPath());
			// Start Move node modules code
			File source = Utility.getActualLocation(configRepository, "TEMP", "");
			log.debug("**** source is ::" + source);
			ArrayList<String> al = new ArrayList<String>();
			if(app.getAppTechnicalTemplate() !=null) {
				log.debug("**** with template flow ::"+app);
				String templateId = app.getAppTechnicalTemplate().getTechnicalTemplateUniqueName();
				for (int i = 1; i <= 10; i++) {
					if (new File(source, "node_modules_" + templateId + "_" + i).exists()) {
					              al.add("node_modules_" + templateId + "_" + i);
					       }
					}	
			}else {
				log.debug("**** with-out template flow ::"+app);
				File file = Utility.getActualLocation(configRepository, "TEMP", "");
				for (int i = 1; i <= 10; i++) {
					if (new File(file, "node_modules_without_template" + "_" + i).exists()) {
			              al.add("node_modules_without_template" + "_" + i);
			       }
				}
				
			}
					
			if (!new File(appFolder.getPath(), "node_modules").exists()) {
				if(al.size()>0) {
					String nodeModule = al.get(0);
					MoveFolder.moveTwoDirectories(appFolder.getPath(), null, new File(source, nodeModule).getPath());
					new File(appFolder.getPath(), nodeModule).renameTo(new File(appFolder.getPath(), "node_modules"));
				}else {
					log.warn("### No node_modules exists in temp folder. Slkipping copy from temp");
				}
			}
			// Ends move node modules code
			// TODO Add logic to dynamically assign port
			log.debug("**** app.getApplicationName() is :: " + app.getApplicationName());
			AppRuntime appRuntime = new AppRuntime().name(app.getApplicationName()+"_FE").runtimeType(RuntimeType.FRONT_END)
					.runTimeCommand("NPM_START").runtimePort(90001).runTimePath(appFolder.getPath());
			log.debug("**** npm start is appRuntime ::" + appRuntime);
			appRuntimeRepository.save(appRuntime);
			//app.addRuntime(appRuntime);
			applicationRepository.save(app);
		} else {
			log.info("Folder {} does not contain package.json file.", appFolder.getPath());
		}
	}
	private void checkForMaven(Application app, File folder) {
		log.debug("**** inside maven **********");
		if (new File(folder, "pom.xml").exists()) {
			log.info("Folder {} contains pom.xml file.", folder.getPath());
			// TODO Add logic to dynamically assign port
			AppRuntime appRuntime = new AppRuntime().name(app.getApplicationName()+"_BE").runtimeType(RuntimeType.BACK_END)
					.runTimeCommand("MAVEN").runtimePort(8050).runTimePath(folder.getPath());
			appRuntimeRepository.save(appRuntime);
			//app.addRuntime(appRuntime);
			applicationRepository.save(app);
		} else {
			log.info("Folder {} does not contain pom.xml file.", folder.getPath());
		}
	}
}
