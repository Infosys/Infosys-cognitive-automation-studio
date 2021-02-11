/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.bpm;

import java.net.URI;
import java.util.Collections;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponents;
import org.springframework.web.util.UriComponentsBuilder;

import com.infosys.impact.botfactory.domain.AutomationWorkFlow;


public class DeployBPMNToCamunda implements JavaDelegate {
	private static final Logger log = LoggerFactory.getLogger(DeployBPMNToCamunda.class);

	public void execute(DelegateExecution execution) throws Exception {
		log.info("DeployBPMNToCamunda - Started deploying the BPMN to local");
		AutomationWorkFlow workflow = (AutomationWorkFlow) execution.getVariable("AutomationWorkFlow");
		byte[] bpmnFileContent = (byte[]) execution.getVariable("BPMModel");

		RestTemplate restTemplate = new RestTemplate();

		MultiValueMap<String, Object> parts = new LinkedMultiValueMap<String, Object>();

		parts.add("xmlData", new String(bpmnFileContent));

		HttpHeaders headers = new HttpHeaders();
		headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
		HttpEntity<MultiValueMap<String, Object>> request = new HttpEntity<MultiValueMap<String, Object>>(parts,
				headers);

		UriComponents uriComponents = UriComponentsBuilder.newInstance().scheme("http").host("localhost").port(8080)
				.path("/api/bpmnUpload/" + workflow.getId()).build(true);

		URI uri = uriComponents.toUri();

		ResponseEntity<String> strResponse = restTemplate.postForEntity(uri, request, String.class);
		int responseCode = strResponse.getStatusCodeValue();
		log.info("responseCode---->" + responseCode);

	}

}
