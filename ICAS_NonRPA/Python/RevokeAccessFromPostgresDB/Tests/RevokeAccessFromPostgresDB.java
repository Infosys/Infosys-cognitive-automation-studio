package com.infosys.impact.botfactory.microbot.testing;

import static org.junit.Assert.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import java.util.HashMap;
import java.util.List;

import org.junit.jupiter.api.Test;

import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.PythonBotExecutor;

public class RevokeAccessFromPostgresDB {
	private static final String False = null;
	@Test
	void testRevokeAccessFromPostgresDB_001_PositiveTestCase() throws Exception {
		
		PythonBotExecutor pythonBotExecutor = new PythonBotExecutor();
		HashMap<String, Object> params = new HashMap<>();
		params.put("dbName", "test_db");
		params.put("dbUsername", "postgres");
		params.put("dbPassword", "root");
		params.put("dbHost", "127.0.0.1");
		params.put("port", "5432");
		params.put("userName", "vikram1");
		params.put("ProcessInstanceId", "revoke_role_access_postgres_user_positive");
		
		String instanceId=(String) params.get("ProcessInstanceId");
		System.out.println(instanceId);
		
		
        HashMap<String, String> taskProps = new HashMap<String, String>();
        HashMap<String, String> configProps = new HashMap<String, String>();
        configProps.put("FilePaths.pythonbotsPath", "C:\\BOTFACTORY\\botfactory-application\\BotFactory_BE\\bot-factory-microbots\\src\\main\\java\\com\\infosys\\impact\\botfactory\\microbot");
		taskProps.put("botName","RevokeAccessFromPostgresDB");
		params.put("TaskProperties", taskProps);
		params.put("config", configProps);
        pythonBotExecutor.executeBot(params);
        
        HashMap output=(HashMap) params.get("RevokeAccessFromPostgresDB_Output");
        
        System.out.println(output );
        
        if(output.containsKey("status")) {
        	assertTrue(true);
        }
        else {
        	assertTrue(false);
        }
        System.out.println("========================");

	}
	@Test
	void testRevokeAccessFromPostgresDB_002_NegativetiveTestCase() throws Exception {
		
		PythonBotExecutor pythonBotExecutor = new PythonBotExecutor();
		HashMap<String, Object> params = new HashMap<>();
		params.put("dbName", "test_db");
		params.put("dbUsername", "postgres");
		params.put("dbPassword", "wrongPwd");
		params.put("dbHost", "127.0.0.1");
		params.put("port", "5432");
		params.put("userName", "vikram1");
		params.put("ProcessInstanceId", "revoke_role_access_user_invalid_value");
		
		String instanceId=(String) params.get("ProcessInstanceId");
		System.out.println(instanceId);
		
		
        HashMap<String, String> taskProps = new HashMap<String, String>();
        HashMap<String, String> configProps = new HashMap<String, String>();
        configProps.put("FilePaths.pythonbotsPath", "C:\\BOTFACTORY\\botfactory-application\\BotFactory_BE\\bot-factory-microbots\\src\\main\\java\\com\\infosys\\impact\\botfactory\\microbot");
		taskProps.put("botName","RevokeAccessFromPostgresDB");
		params.put("TaskProperties", taskProps);
		params.put("config", configProps);
        pythonBotExecutor.executeBot(params);
        
        HashMap output=(HashMap) params.get("RevokeAccessFromPostgresDB_Output");
        
        System.out.println(output );
        
        if(output.containsKey("Exception")) {
        	assertFalse(false);
        }
        else {
        	assertFalse(true);
        }
        
        System.out.println("========================");

	}
	@Test
	void testRevokeAccessFromPostgresDB_003_NegativeTestCase() throws Exception {
		PythonBotExecutor pythonBotExecutor = new PythonBotExecutor();
		HashMap<String, Object> params = new HashMap<>();
		params.put("dbName", "test_db");
		params.put("dbUsername", "postgres");
		params.put("dbPassword", "");
		params.put("dbHost", "127.0.0.1");
		params.put("port", "5432");
		params.put("userName", "vikram1");
		params.put("ProcessInstanceId", "revoke_role_accesss_user_missing_path");
		
		String instanceId=(String) params.get("ProcessInstanceId");
		System.out.println(instanceId);
        HashMap<String, String> taskProps = new HashMap<String, String>();
        HashMap<String, String> configProps = new HashMap<String, String>();
        configProps.put("FilePaths.pythonbotsPath", "C:\\BOTFACTORY\\botfactory-application\\BotFactory_BE\\bot-factory-microbots\\src\\main\\java\\com\\infosys\\impact\\botfactory\\microbot");
		taskProps.put("botName","RevokeAccessFromPostgresDB");
		params.put("TaskProperties", taskProps);
		params.put("config", configProps);
        pythonBotExecutor.executeBot(params);
        
        HashMap output=(HashMap) params.get("RevokeAccessFromPostgresDB_Output");
        System.out.println(output );
        
  
		
        if(output.containsKey("validation")) {
        	assertFalse(false);
        }
        else {
        	assertFalse(true);
        }
        System.out.println("========================");
	}
}
