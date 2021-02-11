/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.exec;

import java.io.File;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

//import com.infosys.impact.botfactory.custom.AppGenerator;
import com.infosys.impact.botfactory.custom.Utility;
//import com.infosys.impact.botfactory.domain.AppRuntime;
import com.infosys.impact.botfactory.domain.Application;
import com.infosys.impact.botfactory.repository.ApplicationRepository;
import com.infosys.impact.botfactory.repository.ConfigurationEntryRepository;
import com.infosys.impact.botfactory.domain.Runtime;
import com.infosys.impact.botfactory.repository.RuntimeRepository;

/**
 * Microbot that generates a JHipster application
 */
@RestController
@RequestMapping("/api")
public class ExecuteAppRuntime {

	private static final Logger log = LoggerFactory.getLogger(ExecuteAppRuntime.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;	
	@Autowired
	private ApplicationRepository applicationRepository;

	@Autowired
	private RuntimeRepository runtimeRepository;
	
	@GetMapping({"/executeApp"})
	public void execute(@RequestParam String appId) throws Exception {
		log.info("ExecuteAppRuntime {}",appId);
		long appID = Long.parseLong(appId);
		Application app = applicationRepository.findById(appID).get();
		String appname = app.getApplicationName() + "_";
		
		//List<Runtime> lstruntime = runtimeRepository.findAll();
		for(Runtime ar:runtimeRepository.findAll()) {
			if(ar.getName().contains(appname))
			{
				//log.info("Processing ",ar);
				Utility.runProcess(ar.getName(), new File(ar.getRunTimePath()), Utility.getConfigValue(configRepository, "Commands", ar.getRunTimeCommand()),false,ar.getName()+".txt");
			}
		}
		
		// for(AppRuntime ar:app.getRuntimes()) {
		// 	log.info("Processing ",ar);
		// 	Utility.runProcess(ar.getName(), new File(ar.getRunTimePath()), Utility.getConfigValue(configRepository, "Commands", ar.getRunTimeCommand()),false,ar.getName()+".txt");
		// }
	}
}
