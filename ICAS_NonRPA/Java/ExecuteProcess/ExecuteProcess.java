/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.devbot.microbots.process;

import java.io.File;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.devbot.custom.AppGenerator;
import com.infosys.impact.devbot.custom.Utility;
import com.infosys.impact.devbot.domain.AppRuntime;
import com.infosys.impact.devbot.domain.Application;
import com.infosys.impact.devbot.repository.ApplicationRepository;
import com.infosys.impact.devbot.repository.ConfigurationEntryRepository;

/**
 * Microbot that generates a JHipster application
 */
@RestController
@RequestMapping("/api")
public class ExecuteProcess{

	private static final Logger log = LoggerFactory.getLogger(AppGenerator.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;	
	@Autowired
	private ApplicationRepository applicationRepository;
	
	@GetMapping({"/execute"})
	public void execute(@RequestParam String appId) throws Exception {
		log.info("ExecuteAppRuntime {}",appId);
		Application app = applicationRepository.findById(appId).get();
		for(AppRuntime ar:app.getRuntimes()) {
			log.info("Processing ",ar);
			Utility.runProcess(ar.getName(), new File(ar.getRunTimePath()), Utility.getConfigValue(configRepository, "Commands", ar.getRunTimeCommand()),false);
		}
	}
}
