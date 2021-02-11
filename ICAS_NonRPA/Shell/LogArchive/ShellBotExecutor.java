package com.infosys.impact.botfactory.microbots.framework;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import com.infosys.impact.botfactory.custom.Utility;
import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class ShellBotExecutor implements BotExecutor {
	private static final Logger log = LoggerFactory.getLogger(ShellBotExecutor.class);

	@Override
	public void executeBot(Map<String, Object> params) {
		String botName = (String) ((Map<String, Object>) params.get("TaskProperties")).get("botName");
		System.out.println("BotName------------------> " + botName);
		
		// To get path where all the Shell bots are placed on Linux/Unix server from Config Entry table 
		// RestTemplate restTemplate = new RestTemplate();
		// final String shellBotlocationUrl = "http://localhost:8080/api/configuration-entries/FilePaths/shellBotsPath";
		// String shellBotPath = null;
		// try {
		// 	ResponseEntity<String> shellBotlocationUrlresponse = restTemplate.getForEntity(new URI(shellBotlocationUrl),
		// 			String.class);
		// 	shellBotPath = shellBotlocationUrlresponse.getBody();
			
		// } catch (URISyntaxException e1) {
		// 	// TODO Auto-generated catch block
		// 	e1.printStackTrace();
		// }

		String shellBotPath = Utility.getConfigurationValue("FilePaths", "shellBotsPath");

	 {
		 String username = (String) params.get("username");
		 String password = (String) params.get("password");
		 String host = (String) params.get("host");
		 String port = (String) params.get("port");
		 int int_port = Integer.parseInt(port);
		 
		 String foldername = (String) params.get("foldername");
		 String src = (String) params.get("src");
		 String dest = (String) params.get("dest");
		 String filename = (String) params.get("filename");
		 
		 
		 
		 String response = null;
		try {
			/**
			 * Create a new Jsch object This object will execute shell commands or scripts
			 * on server
			 */
			JSch jsch = new JSch();
			/*
			 *  Open a new session, with your username, host and port Set the password and
			 * call connect. session.connect() opens a new connection to remote SSH server.
			 * Once the connection is established, you can initiate a new channel. this
			 * channel is needed to connect to remotely execution program
			 */
			Session session = jsch.getSession(username, host, int_port);
			session.setConfig("StrictHostKeyChecking", "no");
			session.setPassword(password);
			session.connect();

			// create the execution channel over the session
			ChannelExec channelExec = (ChannelExec) session.openChannel("exec");

			// Gets an InputStream for this channel. All data arriving in as messages from
			// the remote side can be read from this stream.
			InputStream in = channelExec.getInputStream();

			// Set the command that you want to execute
			// In our case its the remote shell script
			//String path = shellBotPath + botName + ".sh";
			
			//Exporting the file/s or folder/s to be copied from src folder from Camunda
//			String srcExport = "export source=" + src + "/" + foldername;
			String srcExport = "export source=" + foldername;
//			System.out.println(srcExport);
			
//			//Exporting the destination path from Camunda
//			String destExport = "export target=" + dest + "/";
//			System.out.println(destExport);
			
			//Creating path of the command with location of the Shell script located on server
			String path = shellBotPath + botName + ".sh" + " source";
			System.out.println(path);
			
			//Creating command for shell script
			StringBuilder sb = new StringBuilder();
			String command = sb.append("sh" + " " + path).toString();
			System.out.println(command);
			
			//Creating combination of commands to execute them one-by-one using separator as '&&'
			String masterCommand = srcExport + "&&" + command;
			System.out.println(masterCommand);
			channelExec.setCommand(masterCommand);

			//  Execute the command
			channelExec.connect();

			// Read the output from the input stream we set above
			BufferedReader reader = new BufferedReader(new InputStreamReader(in));
			// String line = null;
			String line = null;
			List<String> result = new ArrayList<String>();	
			// Read each line from the buffered reader and add it to result list
			// You can also simple print the result here
			while ((line = reader.readLine()) != null) {
				result.add(line);
			}

			// retrieve the exit status of the remote command corresponding to this channel
			int exitStatus = channelExec.getExitStatus();
			System.out.println("Testing*****************************" + exitStatus);

			// Safely disconnect channel and disconnect session. If not done then it may
			// cause resource leak
			channelExec.disconnect();
			session.disconnect();

			if (exitStatus < 0) {
				
				response = "Done, but exit status not set!";
			}

			else if (exitStatus > 0) {
				response = "Done, but with error!";
			}

			else {
				response ="Done!";
			}

		} catch (Exception e) {
			//response = "Error: " + e);
			params.put("response", e);
		}
		params.put("response", response);
	 }

 }
}