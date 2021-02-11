/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots;

import java.io.File;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.domain.Application;
import com.infosys.impact.botfactory.repository.ApplicationRepository;
import com.infosys.impact.botfactory.repository.ConfigurationEntryRepository;

/**
 * Microbot that generates a JHipster application
 */
@RestController
@RequestMapping("/api")
public class MoveFile {

	private static final Logger log = LoggerFactory.getLogger(MoveFile.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;
	@Autowired
	private ApplicationRepository applicationRepository;

	@GetMapping({ "/proccesFile/*" })
	public void execute(@RequestParam String fileName, @RequestParam String location,
			@RequestParam String targetLocation, @RequestParam Long appId, @RequestParam String relativePath)
			throws Exception {
		Application app = applicationRepository.findById(appId).get();
		String folderName = app.getApplicationName() + "_" + app.getApplicationVersion();
		folderName = folderName.replaceAll(" ", "_");
		folderName = folderName.replaceAll("\\.", "_");
		File parent = Utility.getActualLocation(configRepository, location, folderName);
		File target = Utility.getActualLocation(configRepository, targetLocation, folderName);
		if (!relativePath.equals("/") && !relativePath.equals("")) {
			target = new File(target, relativePath);
		}
		log.info("Moving {} into {}", parent.getPath(), target.getPath());
		new File(parent, fileName).renameTo(new File(target, fileName));
	}
}
