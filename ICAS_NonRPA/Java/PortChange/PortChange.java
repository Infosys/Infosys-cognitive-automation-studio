/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Scanner;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Example;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.domain.Application;
import com.infosys.impact.botfactory.domain.ConfigurationEntry;
import com.infosys.impact.botfactory.microbot.filemodification.ListFiles;
import com.infosys.impact.botfactory.repository.ApplicationRepository;
import com.infosys.impact.botfactory.repository.ConfigurationEntryRepository;

@RestController
@RequestMapping("/api")
public class PortChange {

	private static final Logger log = LoggerFactory.getLogger(PortChange.class);

	@Autowired
	private ConfigurationEntryRepository configRepository;
	@Autowired
	private ApplicationRepository applicationRepository;

	@GetMapping({ "/assignFrontEndPort" })
	public void execute(@RequestParam String appId) throws Exception {
		long appID = Long.parseLong(appId);
		Application appl = (Application) applicationRepository.findById(appID).orElse(null);
		String folderName = appl.getApplicationName() + "_" + appl.getApplicationVersion();
		folderName = folderName.replaceAll(" ", "_");
		folderName = folderName.replaceAll("\\.", "_");
		String frontEndPort = null;
		String backEndPort = null;
		InetAddress ip = InetAddress.getLocalHost();
		String hostname = null;
		String url = null;
		hostname = ip.getHostName();
		File fileapp = Utility.getActualLocation(configRepository, "APP_ROOT", folderName);
		if (appl.getUrl() != null) {
			frontEndPort = appl.getFrontEndPort();
			log.info("*** FrontEndPort :: " + frontEndPort);
			backEndPort = appl.getBackEndPort();
			log.info("*** BackEndPort :: " + backEndPort);
		} else {
			ConfigurationEntry sampleFrondEndEntry = new ConfigurationEntry().category("port_Number").name("FRONTEND");
			ConfigurationEntry frondEndEntry = null;
			Optional<ConfigurationEntry> csFEP = configRepository.findOne(Example.of(sampleFrondEndEntry));

			if (csFEP.isPresent()) {
				frondEndEntry = csFEP.get();
			} else {
				frondEndEntry = sampleFrondEndEntry.value("9001");
			}
			frontEndPort = frondEndEntry.getValue();
			log.info("*** FrontEndPort :: " + frontEndPort);
			ConfigurationEntry sampleBackEndEntry = new ConfigurationEntry().category("port_Number").name("BACKEND");
			ConfigurationEntry backEndEntry = null;
			Optional<ConfigurationEntry> csBEP = configRepository.findOne(Example.of(sampleBackEndEntry));

			if (csBEP.isPresent()) {
				backEndEntry = csBEP.get();
			} else {
				backEndEntry = sampleBackEndEntry.value("5001");
			}
			backEndPort = backEndEntry.getValue();
			log.info("*** BackEndPort :: " + backEndPort);
			
			appl.setBackEndPort(backEndPort);
			appl.setFrontEndPort(frontEndPort);
			int BE_Port = Integer.parseInt(backEndPort) + 1;
			backEndPort = BE_Port + "";
			int FE_Port = Integer.parseInt(frontEndPort) + 1;
			frontEndPort = FE_Port + "";
			backEndEntry.value(backEndPort);
			frondEndEntry.value(frontEndPort);
			configRepository.save(backEndEntry);
			configRepository.save(frondEndEntry);
		}

		String appFolder = fileapp.getPath();
		List<String> files = new ArrayList<>();
		String pattern = ".*";
		ListFiles.listFiles(new File(appFolder), files, pattern);

		for (int i = 0; i < files.size(); i++) {
			File file = new File(files.get(i));
			Scanner scanner;
			try {
				scanner = new Scanner(file);
//				while (scanner.hasNextLine()) {
//					final String lineFromFile = scanner.nextLine();
//					if (lineFromFile.contains("$PortNumber")) {
				// a match!
				String content = Utility.readFile(file.getPath());

				content = content.replaceAll("\\$PortNumber", "" + backEndPort);
				// writeFile(file.getPath(), content);
//					}else if (lineFromFile.contains("$FEPortNumber")) {
				// a match!
				// content = Utility.readFile(file.getPath());
				content = content.replaceAll("\\$FEPortNumber", "" + frontEndPort);
				// writeFile(file.getPath(), content);
//					} else if (lineFromFile.contains("$HostName")) {
				// a match!
				// content = Utility.readFile(file.getPath());
				content = content.replaceAll("\\$HostName", "" + hostname);
				writeFile(file.getPath(), content);
				// }
//				}
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}

		url = "http://" + hostname + ":" + frontEndPort;
		System.out.println("******JAVA***FRONTENDPORT****** URL = " + url);

		appl.setUrl(url);
		applicationRepository.save(appl);

	}

	private static void writeFile(String path, String content) throws IOException {
		FileWriter wr = new FileWriter(path);
		wr.write(content);
		wr.close();
	}

}
