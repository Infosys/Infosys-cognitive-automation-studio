/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.custom;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import org.camunda.bpm.engine.ProcessEngine;
import org.camunda.bpm.engine.ProcessEngines;
import org.camunda.bpm.engine.RuntimeService;
import org.camunda.bpm.engine.runtime.Execution;
import org.camunda.bpm.engine.runtime.ProcessInstance;
import org.camunda.bpm.engine.variable.Variables;
import org.camunda.bpm.engine.variable.value.ObjectValue;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Example;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.infosys.impact.botfactory.domain.Application;
import com.infosys.impact.botfactory.repository.ApplicationRepository;

import com.infosys.impact.botfactory.domain.ConfigurationEntry;
import com.infosys.impact.botfactory.repository.ConfigurationEntryRepository;

import com.infosys.impact.botfactory.domain.Asset;
import com.infosys.impact.botfactory.repository.AssetRepository;

import com.infosys.impact.botfactory.domain.ApplicationComponent;
import com.infosys.impact.botfactory.domain.Artifact;
//import com.infosys.impact.botfactory.repository.AssetRepository;


@Component
public class AppGenerationJob {

	@Autowired
	private ApplicationRepository applicationRepository;

	@Autowired
	private ConfigurationEntryRepository configRepository;

	@Autowired
	private AssetRepository assetRepository;

	private static final Logger log = LoggerFactory.getLogger(AppGenerationJob.class);

	private static final SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");

	@Scheduled(fixedRate = 60000)
	public void executeAppGenerations() {
		log.debug("Checking for any applications pending for code generation");

		Application sample = new Application();
		sample.setCodeGenerationStatus("TBD");
		sample.setApplicationComponents(null);
		/*
		 * sample.setOthers(null); sample.setRuntimes(null); sample.setChannels(null);
		 */
		List<Application> cs = applicationRepository.findAll(Example.of(sample));

		if (cs.size() == 0) {
			log.debug("No apps pending for code generation");
		} else {
			log.debug("{} apps pending for code generation", cs.size());
		}
		for (Application c : cs) {
			log.info("Generation for {}  queued", c.getApplicationName());
			c.setCodeGenerationStatus("Queued");
			c.setApplicationVersion("1.0");
			applicationRepository.save(c);			
		}
		for (Application c : cs) {
			log.info("Generation for {}  started", c.getApplicationName());
			c.setCodeGenerationStatus("InProgress");
			applicationRepository.save(c);
			Map<String, Object> variables = new HashMap<String, Object>();
			ObjectValue application = Variables.objectValue(c)
					.serializationDataFormat(Variables.SerializationDataFormats.JAVA).create();
			variables.put("AppType", "Application");
			variables.put("Application", application);
			variables.put("Configuration", getConfig());
			variables.put("ApplicationName", c.getApplicationName());
			variables.put("ApplicationVersion", c.getApplicationVersion());
			// variables.put("DBTechnology",
			// c.getDbTechnology().getTechnology().getTechnologyName().toLowerCase());
			variables.put("ApplicationComponents", c.getApplicationComponents());
			String folderName = c.getApplicationName() + "_" + c.getApplicationVersion();
			folderName = folderName.replaceAll(" ", "_");
			folderName = folderName.replaceAll("\\.", "_");
			File app = Utility.getActualLocation(configRepository, "APP_ROOT", folderName);
			log.info("Application path is " + app.getPath());
			variables.put("ApplicationPath", app.getPath());

			//Add template Asset
			String assetUniqueName = c.getAppTechnicalTemplate().getAssetUniqueName();
			Asset sampleAsset = new Asset();
			sampleAsset.setAssetUniqueName(assetUniqueName);			
			List<Asset> lstAsset = assetRepository.findAll(Example.of(sampleAsset));
			if(lstAsset.size() > 0)
			{
				variables.put("templateAsset", lstAsset.get(0));
			}

			//Add Application components 
			Set<ApplicationComponent> appComponents =  c.getApplicationComponents();
			variables.put("appComponents", appComponents);

			//Add all Artifacts related to components	
			List<Artifact> appComponentArtifacts = new ArrayList<Artifact>();
			for(ApplicationComponent comp :  c.getApplicationComponents())
			{
				String uniqAssetName = comp.getAssetUniqueName();
				Asset compSampleAsset = new Asset();
				compSampleAsset.setAssetUniqueName(uniqAssetName);			
				List<Asset> lstcompAsset = assetRepository.findAll(Example.of(compSampleAsset));
				for(Asset asset :  lstcompAsset)
				{
					Set<Artifact> compArtifact = asset.getArtifacts();
					appComponentArtifacts.addAll(compArtifact);
				}
				
			}

			// variables.put("URL", c.getDevDBServer().getServer().getUrl());
			ProcessEngine processEngine = ProcessEngines.getDefaultProcessEngine();
			RuntimeService runtimeService = processEngine.getRuntimeService();
			ProcessInstance instance = runtimeService.startProcessInstanceByKey("CreateApplication", variables);

			c.setCodeGenerationStatus("Complete");
			applicationRepository.save(c);
			log.info("Generation for {} completed", c.getApplicationName());
		}
	}

	private Properties getConfig() {
		List<ConfigurationEntry> conf = configRepository.findAll();
		Properties p = new Properties();
		for (ConfigurationEntry ce : conf) {
			p.setProperty(ce.getCategory() + "." + ce.getName(), ce.getValue());
		}
		return p;
	}
}