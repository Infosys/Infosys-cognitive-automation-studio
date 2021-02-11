/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.bpm;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.Collection;
import java.util.Iterator;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.camunda.bpm.model.bpmn.Bpmn;
import org.camunda.bpm.model.bpmn.BpmnModelInstance;
import org.camunda.bpm.model.bpmn.instance.EndEvent;
import org.camunda.bpm.model.bpmn.instance.FlowNode;
import org.camunda.bpm.model.bpmn.instance.SequenceFlow;
import org.camunda.bpm.model.bpmn.instance.bpmndi.BpmnEdge;
import org.camunda.bpm.model.bpmn.instance.bpmndi.BpmnShape;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.domain.Task;


public class AddStepToBpmn implements JavaDelegate {
	private static final Logger log = LoggerFactory.getLogger(AddStepToBpmn.class);

	public void execute(DelegateExecution execution) throws Exception {
		logContext(execution);

		byte[] bpmnFileContent = (byte[]) execution.getVariable("BPMModel");
		// AutomationWorkFlow workflow = (AutomationWorkFlow)
		// execution.getVariable("AutomationWorkFlow");
		Task task = (Task) execution.getVariable("task");
		BpmnModelInstance modelInstance = Bpmn.readModelFromStream(new ByteArrayInputStream(bpmnFileContent));
		String endEventId = null;
		Collection<EndEvent> endElements = modelInstance.getModelElementsByType(EndEvent.class);
		EndEvent endEvent = null;
		if (endElements.size() == 0) {
			log.warn("No End Event found. Skipping addition");
			return;
		} else if (endElements.size() == 1) {
			endEvent = (EndEvent) endElements.toArray()[0];
			endEventId = endEvent.getId();
		} else {
			String endElementToUseForExtension = (String) execution.getVariable("EndElementToUseForExtension");
			if (endElementToUseForExtension == null) {
				log.warn(
						"More than one endEvent is found in BPMN and no End Event mentioned for extension. Skipping addition");
				return;
			}
			for (EndEvent ee : endElements) {
				if (ee.getId().equals(endElementToUseForExtension)) {
					endEvent = ee;
				}
			}
			if (endEvent == null) {
				log.warn("End Event {} not found in the BPMN. Skipping addition", endElementToUseForExtension);
				return;
			}
			endEventId = endEvent.getId();
		}
		//log.info("Found End from which extension needs to be added");

		SequenceFlow sequenceFlow=null;
		Iterator<SequenceFlow> sequenceFlowIt = endEvent.getIncoming().iterator();
		if(sequenceFlowIt.hasNext()){
			sequenceFlow = sequenceFlowIt.next();
		}else{
			log.warn("End Event {} not connected through incoming sequence flows. Skipping addition", endEvent.getId());
			return;
		}
		FlowNode serviceTask = sequenceFlow.getSource();

		serviceTask.getOutgoing().remove(sequenceFlow);
		endEvent.getIncoming().remove(sequenceFlow);
		sequenceFlow.getParentElement().removeChildElement(sequenceFlow);

//		for (Artifact a : task.getTask().getAsset().getArtifacts()) {
//			if (a.getArtifactType().equals(ArtifactType.CONFIGURATION)) {
//				byte[] bs = a.getContent();
//				ByteArrayInputStream bais = new ByteArrayInputStream(bs);
//				Properties p = new Properties();
//				p.load(bais);
//							
//				
//				if ("Java".equals(p.getProperty("Technology")) || "Python".equals(p.getProperty("Technology"))) {
//					ServiceTaskBuilder stb = null;
//					stb = serviceTask.builder().serviceTask(task.getName().replaceAll(" ", "")).name(task.getName());
//					stb.camundaClass(p.getProperty("javaClass"));
//					for (Object key : p.keySet()) {
//						String s = (String) key;
//						if (s.startsWith("inputParam") && s.length() <= 12) {
//							stb.camundaInputParameter(p.getProperty(s), "${" + p.getProperty(s) + "}");
//						} else if (s.startsWith("outputParam") && s.length() <= 13) {
//							stb.camundaOutputParameter(p.getProperty(s), "${" + p.getProperty(s) + "}");
//						}
//					}
//
//					EndEventBuilder eeb = stb.endEvent();
//					modelInstance = eeb.done();
//					endEvent.getParentElement().removeChildElement(endEvent);
//					eeb.id(endEventId);
//
//				} else {
//					CallActivityBuilder callActivityBuilder = serviceTask.builder()
//							.callActivity(task.getName().replaceAll(" ", "")).name(task.getName());
//					
//					
//
//					for (Object key : p.keySet()) {
//						String s = (String) key;
//						if (s.startsWith("inputParam") && s.length() <= 12) {
//							callActivityBuilder.camundaIn(p.getProperty(s), "${" + p.getProperty(s) + "}");
//						} else if (s.startsWith("outputParam") && s.length() <= 13) {
//							callActivityBuilder.camundaOut(p.getProperty(s), "${" + p.getProperty(s) + "}");
//						}
//						
//						if(s.startsWith("botName")) {
//							callActivityBuilder.calledElement(s);
//						}
//					}
//					
//					
//
//					EndEventBuilder eeb = callActivityBuilder.endEvent();
//					modelInstance = eeb.done();
//					endEvent.getParentElement().removeChildElement(endEvent);
//					eeb.id(endEventId);
//				}
//
//			}
//		}

		Collection<BpmnShape> bpmnShapes = modelInstance.getModelElementsByType(BpmnShape.class);
		for (BpmnShape shape : bpmnShapes) {
			if (shape.getBpmnElement() == null) {
				shape.getParentElement().removeChildElement(shape);
			}
		}
		Collection<BpmnEdge> bpmnEdges = modelInstance.getModelElementsByType(BpmnEdge.class);
		for (BpmnEdge edge : bpmnEdges) {
			if (edge.getBpmnElement() == null) {
				edge.getParentElement().removeChildElement(edge);
			}
		}
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		Bpmn.writeModelToStream(baos, modelInstance);

		// Bpmn.writeModelToFile(new
		// File("C:\\Users\\silambarasu.t\\Desktop\\"+workflow.getWorkflowName()+".bpmn"),
		// modelInstance);
		log.info("baos.toByteArray()-->" + baos.toByteArray());
		execution.setVariable("BPMModel", baos.toByteArray());

	}
	

	protected void logContext(DelegateExecution execution) {
		log.info("************\n\n   WriteArtifactToFile invoked by " + "processDefinitionId="
				+ execution.getProcessDefinitionId() + ", activtyId=" + execution.getCurrentActivityId()
				+ ", activtyName='" + execution.getCurrentActivityName() + "'" + ", processInstanceId="
				+ execution.getProcessInstanceId() + ", businessKey=" + execution.getProcessBusinessKey()
				+ ", executionId=" + execution.getId() + ", var=" + execution.getVariables() + " \n\n***********");
	}

}
