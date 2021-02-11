/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.devbot.microbots;

import java.io.File;
/*
 * Changes the front end port number of the application
 */
import java.io.FileWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.devbot.custom.AppGenerator;
import com.infosys.impact.devbot.custom.Utility;
import com.infosys.impact.devbot.domain.Application;
import com.infosys.impact.devbot.repository.ApplicationRepository;
import com.infosys.impact.devbot.repository.ConfigurationEntryRepository;

@RestController
@RequestMapping("/api")
public class FrontEndPortChange {
	
	private static final Logger log = LoggerFactory.getLogger(AppGenerator.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;	
	@Autowired
	private ApplicationRepository applicationRepository;
	@GetMapping({"/assignJHipsterFrontEndPort"})
	public void execute(@RequestParam String appId) throws Exception {
		
		//String file = (String) execution.getVariable("App");
		
		Application appl = (Application) applicationRepository.findById(appId).orElse(null);
		String folderName = appl.getApplicationName() + "_" + appl.getApplicationVersion();
		folderName = folderName.replaceAll(" ", "_");
		folderName = folderName.replaceAll("\\.", "_");
		File fileapp = Utility.getActualLocation(configRepository, "APP_ROOT", folderName);
		
		int counter = 9001;
		int counter1 = 9061;
		InetAddress ip=InetAddress.getLocalHost();
		String hostname=null;
		String url=null;
		
		try {
			String webpackFile = new File(fileapp,"webpack\\webpack.dev.js").getPath();
			String content = Utility.readFile(webpackFile);
			hostname = ip.getHostName();

			String substitute = "port: " + counter;
			content = content.replaceAll("port: 9000", substitute);
			String substitute1 = "localhost:" + counter1;
			content = content.replaceAll("localhost:9060", substitute1);
			writeFile(webpackFile, content);
			String packageFile = new File(fileapp,"package.json").getPath(); 
			content = Utility.readFile(packageFile);
			content = content.replaceAll("9060", "" + counter1);
			content = content.replaceAll("9000", "" + counter);
			writeFile(packageFile, content);
			
			url="http://"+hostname+":"+counter1;
			
			System.out.println("************ URL = "+url);
			
			appl.setUrl(url);
			applicationRepository.save(appl);
			
			
			counter++;
			counter1++;
			
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private static void writeFile(String path, String content) throws IOException {
		FileWriter wr = new FileWriter(path);
		wr.write(content);
		wr.close();
	}

}
