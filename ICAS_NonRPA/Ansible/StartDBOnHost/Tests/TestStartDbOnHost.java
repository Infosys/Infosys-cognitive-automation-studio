/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.testing;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import java.util.HashMap;
import com.infosys.impact.botfactory.microbots.framework.AnsibleBotExecutor;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;

import org.junit.Test;


public class TestStartDbOnHost {
	
	@Test
	public void testStartDbOnHost_PositiveTestCase() throws ExecutionError {
		AnsibleBotExecutor ansibleBotExecutor = new AnsibleBotExecutor();
		HashMap<String, Object> params = new HashMap<String, Object>();
		params.put("AnsibleServerUserName","admin");
		params.put("AnsibleServerPwd", "June@2020");
		params.put("AnsibleServerHostName", "10.138.13.46");
		params.put("AnsibleTargetHost", "dbserver");
		params.put("AnsibleRootPwd", "June@2020");
		
		HashMap<String, String> taskProps = new HashMap<String, String>();
		taskProps.put("botName","StartDBOnHost");
		params.put("TaskProperties", taskProps);
		ansibleBotExecutor.executeBot(params);
		String response = (String) params.get("response");
		System.out.println("response is : "+response);

		
	}
	
	
	@Test
	public void testStartDbOnHost_NegativeTestCase() throws ExecutionError {
		AnsibleBotExecutor ansibleBotExecutor = new AnsibleBotExecutor();
		HashMap<String, Object> params = new HashMap<String, Object>();
		params.put("AnsibleServerUserName","admin");
		params.put("AnsibleServerPwd", "June@2020");
		params.put("AnsibleServerHostName", "10.138.13.46");
		params.put("AnsibleTargetHost", "dbserver");
		params.put("AnsibleRootPwd", "June@2020");
		
		HashMap<String, String> taskProps = new HashMap<String, String>();
		taskProps.put("botName","StartDBOnHost");
		params.put("TaskProperties", taskProps);
		ansibleBotExecutor.executeBot(params);
		String response = (String) params.get("response");
		System.out.println("response is : "+response);

		
	}


}
