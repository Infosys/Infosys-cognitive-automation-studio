/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AssignmentBotProcess implements JavaDelegate {
	private static final Logger log = LoggerFactory.getLogger(AssignmentBotProcess.class);
	public void execute(DelegateExecution execution) throws Exception {
		log.info("*********************AssignmentBotProcess**************************");
		String ticketdescription = (String) execution.getVariable("Description");
		//String header = (String) execution.getVariable("Header");
		String resolution=null;
		log.info("ticketdescription-->"+ticketdescription);
		ticketdescription = ticketdescription.toLowerCase();
		if((ticketdescription.indexOf("need access") != -1) || (ticketdescription.indexOf("can't access") != -1))
			{
				resolution = "CleanDiskSpace_Base";
			}
			else if ( (ticketdescription.indexOf("application") != -1) || (ticketdescription.indexOf("server is down.") != -1) || (ticketdescription.indexOf("Performance problems with") != -1) || (ticketdescription.indexOf("Issue with") != -1) )
			{
				resolution = "Restart_Server_Bot";
				
			}
		log.info("resolution-->"+resolution);	
		execution.setVariable("ResolutionTicket", resolution);
		log.info("*********************End AssignmentBotProcess**************************");
		
	}

}
