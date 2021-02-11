/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.java;
/*
 * create entity using database
 */
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Properties;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;


public class CreateEntity  {

	private static final Logger log = LoggerFactory.getLogger(CreateEntity.class);

	public Status execute(
			@InputParameter(name="Configuration") Properties conf,
			@InputParameter(name="AppDir") String destDir			
			) throws Exception {

		String pomData = readFile(conf.getProperty("Templates.PomData"));
		String temp = conf.getProperty("FilePaths.TEMP");
		writeFile(new File(temp, "pomData.xml").getPath(), pomData);
		String pomContentPath = temp + "\\pomData.xml";

	

		File workingDir = new File(destDir);

		String appPomPath = workingDir.getPath() + "\\pom.xml";
		log.info("Create Entity started");
		String DTDFileContent = readFile(conf.getProperty("Templates.DTD"));
		writeFile(new File(workingDir, "hibernate-reverse-engineering-3.0.dtd").getPath(), DTDFileContent);

		String target = destDir + "\\src\\main\\resources\\config";
		File targetDir = new File(target);

		String hibernateFileContent = readFile(conf.getProperty("Templates.HiberConfig"));

		writeFile(new File(targetDir, "hibernate-config.xml").getPath(), hibernateFileContent);

		String modelFileContent = readFile(conf.getProperty("Templates.ModelConfig"));
		writeFile(new File(targetDir, "model-config.xml").getPath(), modelFileContent);

		log.info("Copied the required files ");

		try {
			Document pomContent = Utility.createDocumentFromFile(pomContentPath);
			Document appPom = Utility.createDocumentFromFile(appPomPath);
			NodeList idList = (NodeList) appPom.getElementsByTagName("id");
			Boolean flag = true;

			// To check if entity profile already exists
			for (int i = 0; i < idList.getLength(); i++) {
				Node node = idList.item(i);
				if (node.getTextContent().equals("entity")) {
					flag = false;

				}
			}

			if (flag) {

				Element entityElement = (Element) pomContent.getElementsByTagName("profile").item(0);

				Element profilesElement = (Element) appPom.getElementsByTagName("profiles").item(0);
				Node profileEntity = appPom.importNode(entityElement, true);
				profilesElement.appendChild(profileEntity);
				// TODO add loop here
				NodeList activeList = (NodeList) appPom.getElementsByTagName("activeByDefault");

				for (int i = 0; i < activeList.getLength(); i++) {
					Node node = activeList.item(i);
					if (node.getTextContent().equals("true")) {
						node.setTextContent("false");

					}
				}

				NodeList missingWebpackList = appPom.getElementsByTagName("missing");
				HashMap<String, Node> missingMap = new HashMap<String, Node>();
				String missDataTemp = "";
				for (int i = 0; i < missingWebpackList.getLength(); i++) {
					Node node = missingWebpackList.item(i);
					missDataTemp = node.getTextContent();
					node.setTextContent("");
					missingMap.put(missDataTemp, node);
				}

				TransformerFactory transformerFactory = TransformerFactory.newInstance();
				Transformer transformer = transformerFactory.newTransformer();
				transformer.setOutputProperty(OutputKeys.INDENT, "yes");
				transformer.transform(new DOMSource(appPom), new StreamResult(new File(appPomPath)));

				String cmd = conf.getProperty("Commands.HiberEntity");

				Utility.runProcess("", workingDir, cmd, true);

				// TODO loop through all nodes where it was true earlier
				for (int i = 0; i < activeList.getLength(); i++) {
					Node node = activeList.item(i);

					node.setTextContent("true");

				}
				for (String data : missingMap.keySet()) {
					missDataTemp = data;
					Node node = missingMap.get(data);
					node.setTextContent(missDataTemp);
				}

				Transformer t = transformerFactory.newTransformer();
				t.setOutputProperty(OutputKeys.INDENT, "yes");
				t.transform(new DOMSource(appPom), new StreamResult(new File(appPomPath)));

			}

			File tempFile = new File(pomContentPath);
			tempFile.delete();

			log.info("Entities are created in path ==> src/main/java/com/infosys/impact/botorch/domain ");
			return new Status("00","create entity success");
		} catch (ParserConfigurationException | SAXException | IOException | TransformerException e) {
			log.error("Error occured in createEntity Process");
			return new Status("Error",e.getMessage(),e);
		}
	
	}

	private static void writeFile(String path, String content) throws IOException {
		FileWriter wr = new FileWriter(path);
		wr.write(content);
		wr.close();
	}

	private static String readFile(String path) throws IOException {
		System.out.println(path);
		BufferedReader reader = new BufferedReader(new FileReader(path));
		StringBuffer sb = new StringBuffer();
		String l = null;
		do {
			l = reader.readLine();
			if (l != null) {
				sb.append(l + "\n");
			}
		} while (l != null);
		reader.close();
		return sb.toString();
	}

}
