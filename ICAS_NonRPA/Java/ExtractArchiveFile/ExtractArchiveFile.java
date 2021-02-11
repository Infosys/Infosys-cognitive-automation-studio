/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.devbot.microbots;

import java.io.File;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.devbot.custom.AppGenerator;
import com.infosys.impact.devbot.custom.ArchiveUtility;
import com.infosys.impact.devbot.custom.Utility;
import com.infosys.impact.devbot.domain.AppRuntime;
import com.infosys.impact.devbot.domain.Application;
import com.infosys.impact.devbot.domain.enumeration.RuntimeType;
import com.infosys.impact.devbot.repository.AppRuntimeRepository;
import com.infosys.impact.devbot.repository.ApplicationRepository;
import com.infosys.impact.devbot.repository.ConfigurationEntryRepository;

/**
 * Microbot that generates a JHipster application
 */
@RestController
@RequestMapping("/api")
public class ExtractArchiveFile {

	private static final Logger log = LoggerFactory.getLogger(ExtractArchiveFile.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;	
	@Autowired
	private ApplicationRepository applicationRepository;
	@Autowired
	private AppRuntimeRepository appRuntimeRepository;
	
	@GetMapping({"/proccesFile/zip","/proccesFile/jar"})
	public String execute(@RequestParam String fileName, @RequestParam String location, @RequestParam String targetLocation, @RequestParam String appId, @RequestParam String relativePath) throws Exception {
		Application app = applicationRepository.findById(appId).get();
		String folderName = app.getApplicationName()+"_"+app.getApplicationVersion();
		folderName=folderName.replaceAll(" ", "_");
		folderName=folderName.replaceAll("\\.", "_");		
		File parent =  Utility.getActualLocation(configRepository,location,folderName);
		File target =  Utility.getActualLocation(configRepository,targetLocation,folderName);
		if(!relativePath.equals("/") && !relativePath.equals("")) {
			target = new File(target, relativePath);
		};
		target.mkdirs();
		log.info("Extracting {} \\ {} into {}",parent.getPath(),fileName,target.getPath());
		ArchiveUtility.extractArchive(new File(parent,fileName).getPath(), "", target.getPath());
		
		//TODO move this to new micro bots and add logic to handle already added runtimes
//		if(new File(target,"package.json").exists()) {
//			log.info("Folder {} contains package.json file. Copying the node_modules folder",target.getPath());	
//			File f = new File(Utility.getActualLocation(configRepository,"TEMP",""),"node_modules");
//			f.renameTo(new File(target,"node_modules"));
//			//TODO Add logic to dynamically assign port
//			AppRuntime appRuntime=new AppRuntime().name(app.getApplicationName()+"_FrontEnd-Angular").runtimeType(RuntimeType.FRONT_END).runTimeCommand("NPM_START").runtimePort(90001).runTimePath(target.getPath());
//			appRuntimeRepository.save(appRuntime);
//			app.addRuntime(appRuntime);
//			applicationRepository.save(app);
//		}else {
//			log.info("Folder {} does not contain package.json file.",target.getPath());	
//		}
		
//		if(new File(target,"pom.xml").exists()) {
//			log.info("Folder {} contains pom.xml file.",target.getPath());
//			//TODO Add logic to dynamically assign port
//			AppRuntime appRuntime=new AppRuntime().name(app.getApplicationName()+"_BackEnd-Maven").runtimeType(RuntimeType.BACK_END).runTimeCommand("MAVEN").runtimePort(80801).runTimePath(target.getPath());
//			appRuntimeRepository.save(appRuntime);
//			app.addRuntime(appRuntime);
//			applicationRepository.save(app);	
//		}else {
//			log.info("Folder {} does not contain pom.xml file.",target.getPath());	
//		}		
		log.info("Deleting file");
		new File(parent,fileName).delete();
		log.info("Deleted the file");
		return "Done";
	}
}
