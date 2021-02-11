/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StopService implements JavaDelegate {

	private static final Logger log = LoggerFactory.getLogger(StopService.class);

	private static final String TASKLIST = "tasklist";
	private static final String KILL = "taskkill /F /IM ";

	public void execute(DelegateExecution execution) throws Exception {

		String processName = (String) execution.getVariable("processName");

		log.info("StopService called...........................................processName=" + processName);

		if (isProcessRunning(processName)) {

			killProcess(processName);
		}
	}

	public static boolean isProcessRunning(String serviceName) throws Exception {

		log.info("StopService.isProcessRunning() checking ................................................");
		Process p = Runtime.getRuntime().exec(TASKLIST);
		BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
		String line;
		while ((line = reader.readLine()) != null) {
			if (line.contains(serviceName)) {
				return true;
			}
		}

		return false;

	}

	public static void killProcess(String serviceName) throws Exception {

		log.info("StopService.killProcess() called...");

		Runtime.getRuntime().exec(KILL + serviceName);

	}

}
