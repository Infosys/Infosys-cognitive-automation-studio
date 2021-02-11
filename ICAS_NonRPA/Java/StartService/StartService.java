/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot;

import java.io.File;
import java.io.IOException;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StartService implements JavaDelegate {

	private static final Logger log = LoggerFactory.getLogger(StartService.class);

	public void execute(DelegateExecution execution) throws Exception {
		String command = (String) execution.getVariable("processName");
		log.info("StartService called............................................command="+command);
		File file = new File(command);

		if (!file.exists()) {
			throw new IllegalArgumentException("The file " + command + " does not exist");
		}
		try {
			Process p = Runtime.getRuntime().exec(file.getAbsolutePath());
			log.info("Service Started................................");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}