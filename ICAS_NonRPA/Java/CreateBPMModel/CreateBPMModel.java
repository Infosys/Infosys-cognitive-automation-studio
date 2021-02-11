/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.bpm;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.util.Properties;

//import org.activiti.bpmn.model.BpmnModel;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.camunda.bpm.engine.variable.Variables;
import org.camunda.bpm.engine.variable.value.ObjectValue;
import org.camunda.bpm.model.bpmn.Bpmn;
import org.camunda.bpm.model.bpmn.BpmnModelInstance;
import org.camunda.bpm.model.bpmn.builder.ProcessBuilder;
import org.camunda.bpm.model.bpmn.builder.ServiceTaskBuilder;
import org.camunda.bpm.model.bpmn.builder.StartEventBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.domain.AutomationWorkFlow;

/*import com.infosys.impact.devbot.custom.AppGenerator;
import com.infosys.impact.devbot.domain.Artifact;
import com.infosys.impact.devbot.domain.AutomationWorkFlow;
import com.infosys.impact.devbot.domain.Bot;
import com.infosys.impact.devbot.domain.enumeration.ArtifactType;*/

public class CreateBPMModel implements JavaDelegate   {
	private static final Logger log = LoggerFactory.getLogger(CreateBPMModel.class);

	public void execute(DelegateExecution execution) throws Exception {
		  logContext(execution);		  
		  AutomationWorkFlow workflow = (AutomationWorkFlow) execution.getVariable("AutomationWorkFlow");
		  BpmnModelInstance model;
		  String id = workflow.getWorkflowName()+"_"+workflow.getWorkflowVersion();
		  id=id.replaceAll("\\.", "");
		  id=id.replaceAll(" ", "");
		  ProcessBuilder pb =Bpmn.createProcess("Prcess_"+id).executable();	
		  System.out.println("NAME===="+workflow.getWorkflowName()+"  id="+id);
		  StartEventBuilder seb = pb.name(workflow.getWorkflowName()).id(id).
				  							startEvent().id("workflow1_startevent1").name("Start Event");
		  ServiceTaskBuilder stb=null;
		
		  model = seb.endEvent().id("workflow1_endevent1").name("End Event").done().clone();		  
		
		  ByteArrayOutputStream baos=new ByteArrayOutputStream();
		  Bpmn.writeModelToStream(baos, model);		
		  
		  execution.setVariable("BPMModel",baos.toByteArray());		
	 }
	  protected void logContext(DelegateExecution execution) {
		  log.info("************\n\n   WriteArtifactToFile invoked by "
		            + "processDefinitionId=" + execution.getProcessDefinitionId()
		            + ", activtyId=" + execution.getCurrentActivityId()
		            + ", activtyName='" + execution.getCurrentActivityName() + "'"
		            + ", processInstanceId=" + execution.getProcessInstanceId()
		            + ", businessKey=" + execution.getProcessBusinessKey()
		            + ", executionId=" + execution.getId()
		            + ", var=" + execution.getVariables()
		            + " \n\n***********");
	  }
	  
}
