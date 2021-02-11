/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.framework;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;


/**
 * This class executes the shell script on the remote server Requires the jSch
 * java library
 *
 */
public class AnsibleBotExecutor implements BotExecutor {

	private static final Logger log = LoggerFactory.getLogger(AnsibleBotExecutor.class);
	private static int ansibleSSHPort=22;

	@Override
	public void executeBot(Map<String, Object> params) throws ExecutionError  {
		// TODO Auto-generated method stub		
		
		String ansibleServerUser = (String) params.get("AnsibleServerUserName");
		String ansibleServerPwd = (String) params.get("AnsibleServerPwd");
		String ansibleServerHostName = (String) params.get("AnsibleServerHostName");
		String ansibleTargetHostGroup = (String) params.get("AnsibleTargetHost");
		String ansibleRootPwd = (String) params.get("AnsibleRootPwd");
		String ansiblePlayBookName = (String) params.get("AnsiblePlayBookName");
		
		String response =  executeTask(ansibleServerUser,ansibleServerPwd,ansibleServerHostName,ansibleTargetHostGroup,ansibleRootPwd,ansiblePlayBookName);
		params.put("response", response);
	}

	public String executeTask(String ansibleServerUser,String ansibleServerPwd, String ansibleServerHostName,String ansibleTargetHostGroup,String ansibleRootPwd,String ansiblePlayBookName) {
		//System.out.println("File path : " + scriptFileName);
		String line = "";
		List<String> ansibleOutput = new ArrayList<String>();		
		String result = "";
		try {
			/**
			 * Create a new Jsch object This object will execute shell commands or scripts
			 * on server
			 */
			JSch jsch = new JSch();
			/*
			 * Open a new session, with your username, host and port Set the password and
			 * call connect. session.connect() opens a new connection to remote SSH server.
			 * Once the connection is established, you can initiate a new channel. this
			 * channel is needed to connect to remotely execution program
			 */
			Session session = jsch.getSession(ansibleServerUser, ansibleServerHostName, ansibleSSHPort);
			session.setConfig("StrictHostKeyChecking", "no");
			session.setPassword(ansibleServerPwd);
			session.connect();

			// create the execution channel over the session
			ChannelExec channelExec = (ChannelExec) session.openChannel("exec");

			// Gets an InputStream for this channel. All data arriving in as messages from
			// the remote side can be read from this stream.
			InputStream in = channelExec.getInputStream();

			// Set the command that you want to execute
			// In our case its the remote shell script
			StringBuilder sb = new StringBuilder();		
			String command = sb.append(
					"ansible-playbook "+ ansiblePlayBookName +" --extra-var 'host_name="+ ansibleTargetHostGroup +" ansible_become_pass="+ ansibleRootPwd +"'")
					.toString();

			// echo "hello $1"
			// String command = sb.append("echo 'hello $1'").toString();
			channelExec.setCommand(command);

			// Execute the command
			channelExec.connect();

			// Read the output from the input stream we set above
			BufferedReader reader = new BufferedReader(new InputStreamReader(in));
		
			// Read each line from the buffered reader and add it to result list
			// You can also simple print the result here
			while ((line = reader.readLine()) != null) {
				ansibleOutput.add(line);
			}

			// retrieve the exit status of the remote command corresponding to this channel
			int exitStatus = channelExec.getExitStatus();
			
			channelExec.disconnect();
			session.disconnect();

			if (exitStatus < 0) {
				log.info("Done, but exit status not set!");
				result = "Done, but with error! " + exitStatus;
			}

			else if (exitStatus > 0) {
				log.info("Done, but with error!");
				result = "Done, but with error! " + exitStatus;
			}

			else {
				
				log.info("**********Task Completed Succesfully ************* ");				
				result = "********** Task Completed Succesfully ************* ";				
				
			}

		} catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			result = "Display Error code ::" + className;
		}
		System.out.println("**********Ansible Installation Results " + result + ansibleOutput.toString());
		return result + ansibleOutput.toString();		
	}

}
