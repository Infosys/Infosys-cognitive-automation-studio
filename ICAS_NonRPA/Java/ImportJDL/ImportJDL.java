/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.java;

/*
 * Create entities for Jhipster application by importing a JDL file(File extension => .jh)
 */
import java.io.File;
import java.util.Optional;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.domain.Application;
import com.infosys.impact.botfactory.domain.TechnologyStack;
import com.infosys.impact.botfactory.repository.ApplicationRepository;
import com.infosys.impact.botfactory.repository.ConfigurationEntryRepository;
import com.infosys.impact.botfactory.repository.TechnologyStackRepository;

import org.springframework.data.domain.Example;
/*import com.infosys.impact.devbot.custom.AppGenerator;
import com.infosys.impact.devbot.custom.Utility;
import com.infosys.impact.devbot.domain.Application;
import com.infosys.impact.devbot.repository.ApplicationRepository;
import com.infosys.impact.devbot.repository.ConfigurationEntryRepository;*/

@RestController
@RequestMapping("/api")
public class ImportJDL {

	public static final Logger log = LoggerFactory.getLogger(ImportJDL.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;

	@Autowired
	private ApplicationRepository applicationRepository;

	@Autowired
	private TechnologyStackRepository techStackRepository;

	@GetMapping({ "/proccesFile/jh" })
	public void execute(@RequestParam String fileName, @RequestParam String location,
			@RequestParam String targetLocation, @RequestParam Long appId) throws Exception {
		Application app = applicationRepository.findById(appId).get();

		String jhipsterCommand = Utility.getConfigValue(configRepository, "Commands", "JHIPSTER");
		String folderName = app.getApplicationName() + "_" + app.getApplicationVersion();
		folderName = folderName.replaceAll(" ", "_");
		folderName = folderName.replaceAll("\\.", "_");
		File workingDirectory = Utility.getActualLocation(configRepository, "APP_ROOT", folderName);
		File jdlPath = new File(Utility.getActualLocation(configRepository, location, app.getApplicationName()),
				fileName);
		String yoRcJson = Utility.getConfigValue(configRepository, "Templates", "YO_RC_JSON");
		jhipsterCommand = jhipsterCommand + " import-jdl " + jdlPath.getPath() + " --force";
		try {
			String content = Utility.readFile(yoRcJson);
			content = content.replaceAll("\\$AppName", app.getApplicationName());
			TechnologyStack sample = new TechnologyStack();
			sample.setTechnologyStackUniqueName(app.getTechnologyStack());
			Optional<TechnologyStack> stackName = techStackRepository.findOne(Example.of(sample));
						
			content = content.replaceAll("\\$databaseType", stackName.get().getDbTechnology().toLowerCase());					
					//app.getDbTechnology().getTechnology().getTechnologyName().toLowerCase());
			
			//here we have to take get technology stack 1st den get db tech...
			// TODO Add package and other params
//			Utility.writeFile(new File(workingDirectory, ".yo-rc.json").getPath(), content.getBytes());
			Utility.runProcess(app.getApplicationName(), workingDirectory, jhipsterCommand, true);
		} catch (Exception e) {
			e.printStackTrace();
		}
		jdlPath.delete();
	}
}
