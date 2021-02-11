/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.sap_pi;
import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.List;

import javax.xml.bind.JAXBElement;
import javax.xml.datatype.DatatypeConfigurationException;
import javax.xml.datatype.DatatypeFactory;
import javax.xml.datatype.XMLGregorianCalendar;
import javax.xml.namespace.QName;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.oxm.jaxb.Jaxb2Marshaller;


import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.AdapterFilter;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.AdapterFrameworkData;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.GetMessageList;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.GetMessageListResponse;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.MessageInterface;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.MessageParty;

@Bot(name = "GetMessageListFromSAPPI", version = "1.0", description = "", botCategory = "SAP", author = "", technology = "Java", 
technologyCode = "01", botCategoryCode = "0C", botId = "01")
public class GetMessageListFromSAPPI{
	private static final Logger log = LoggerFactory.getLogger(GetMessageListFromSAPPI.class);
    public static void main(String[] args) {    	
    	GetMessageListFromSAPPI application= new GetMessageListFromSAPPI();
    	Jaxb2Marshaller marshaller= new Jaxb2Marshaller();
    	marshaller.setContextPath("com.infosys.impact.botfactory.microbots.sap_pi.gen");
    	String url="http://brsdhtcsaph1:50000/AdapterMessageMonitoring/basic?style=document";
    	SOAPConnector soapConnector = application.soapConnector(marshaller,url);
    	Interface obj=new Interface();
    
    	obj.setSenderInterface("SI_IA_PurchaseOrderRequest");
    

    	String username="INF1037562";
    	String password="Anish@27";
    	List<Message> messages = application.lookup(soapConnector,obj,url,"10","24",username,password);
//    	for(Message msg:messages) {
//    		System.out.println("Inside main");
//    		System.out.println(msg.getMessageID());
//    	}
    }   
    @Errors(exceptions= {
			@Error(errorCode = "010C0111FF", errorMessagePattern = ".*", exceptionClass = IOException.class)
	})
    public Status execute(
			@InputParameter(name = "Interfaceobj")Object Interfaceobj,
			@InputParameter(name = "ParentID",required = false)String parentID,
			@InputParameter(name = "Url") String url,
			@InputParameter(name = "MaxNoOfMessage")String maxNoOfMessage,
			@InputParameter(name = "TimeDuration")String timeDuration,
			@InputParameter(name = "Username")String username,
			@InputParameter(name = "Password")String password,
			
			@OutputParameter(name = "MessageList") ObjectHolder<List<Message>> messageList,
			@OutputParameter(name = "URL") ObjectHolder<String> URL,
			@OutputParameter(name = "InterfaceObjectOutput")ObjectHolder<Object> interfaceObjectOutput
			) throws ExecutionError,IOException{
    	try {
    	GetMessageListFromSAPPI application= new GetMessageListFromSAPPI();
    	Jaxb2Marshaller marshaller= new Jaxb2Marshaller();
    	marshaller.setContextPath("com.infosys.impact.botfactory.microbots.sap_pi.gen");
    	SOAPConnector soapConnector = application.soapConnector(marshaller,url);
    	
    	Interface interfaceObject = (Interface)Interfaceobj;//update the parameter
    	List<Message> messages = application.lookup(soapConnector,interfaceObject,url,maxNoOfMessage,timeDuration,username,password);
    	List<Message> outputMessages = new ArrayList();
    	interfaceObjectOutput.setValue(interfaceObject);
//    	if(parentID!= null) {
//    		
//    	
//    	for(Message m : messages) {
//    		if(m.getParentID().equals(parentID)) {
//    			outputMessages.add(m);
//    		}
//    		
//    		
//    	}}
//    	else
//    	{
//    		outputMessages.addAll(messages);
//    	}
    	messageList.setValue(messages);
    	URL.setValue(url);
    	return new Status("00","Created a list of maps");	}
    		catch(Exception e){
    			
    		return new Status("Error",e.getMessage(),e);
    	}
    }
    
    public SOAPConnector soapConnector(Jaxb2Marshaller marshaller,String url) {
        SOAPConnector client = new SOAPConnector();
        //client.setDefaultUri("http://localhost:50000/AdapterMessageMonitoring/basic?style=document");
		client.setDefaultUri(url);       
        client.setMarshaller(marshaller);
        client.setUnmarshaller(marshaller);
        return client;
    }
    private List<Message> lookup(SOAPConnector soapConnector,Interface Interfaceobj,String url,String maxNoOfMessage,String timeDuration,String username,String password) {
    	List<Message> messages = new ArrayList<>();
        GetMessageList request = new GetMessageList();
        
        JAXBElement<Integer> maxMessages = new JAXBElement<Integer>(new QName("maxMessages"),Integer.class,Integer.parseInt(maxNoOfMessage));//parameterize max messages
        AdapterFilter filter= new AdapterFilter();
        GregorianCalendar from=new GregorianCalendar();
       
        from.add(Calendar.HOUR_OF_DAY, -Integer.parseInt(timeDuration));//parameterize it in terms of hours
		System.out.println(Interfaceobj.getSenderInterface());
        GregorianCalendar to=new GregorianCalendar();
        XMLGregorianCalendar fromX=null;
        XMLGregorianCalendar toX=null;
		try {
			DatatypeFactory df = DatatypeFactory.newInstance();
			fromX = df.newXMLGregorianCalendar(from);
			toX= df.newXMLGregorianCalendar(to);
		} catch (DatatypeConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println(fromX+"Dates"+toX);
        filter.setFromTime(new JAXBElement<XMLGregorianCalendar>(new QName("fromTime"), XMLGregorianCalendar.class, fromX));
        filter.setToTime(new JAXBElement<XMLGregorianCalendar>(new QName("toTime"), XMLGregorianCalendar.class, toX));
        String receiverInterface = Interfaceobj.getReceiverInterface();
        MessageInterface senderMessage=new MessageInterface();
        senderMessage.setName(new JAXBElement<String>(new QName("name"),String.class,receiverInterface));
        //TODO naspace.paty, component 
        //filter.setInterface(new JAXBElement<MessageInterface>(new QName("urn:com.sap.aii.mdt.server.adapterframework.ws","interface"),MessageInterface.class,senderMessage));
        
        String senderParty=Interfaceobj.getSenderParty();
        String namespace=Interfaceobj.getReceiverNamespace();
        String sendercomponent=Interfaceobj.getSenderComponent();
        senderMessage.setSenderParty(new JAXBElement<String>(new QName("senderParty"),String.class,senderParty));
        senderMessage.setNamespace(new JAXBElement<String>(new QName("namespace"),String.class,namespace));
        senderMessage.setSenderComponent(new JAXBElement<String>(new QName("senderComponent"),String.class,sendercomponent));
        filter.setInterface(new JAXBElement<MessageInterface>(new QName("urn:com.sap.aii.mdt.server.adapterframework.ws","interface"),MessageInterface.class,senderMessage));
        //filter.setNamespace(interfaceObject.getSenderNamespace());
        //set senderparty and set interface and set namespace
        //filter.setInterface(senderInterface);
        request.setMaxMessages(maxMessages);
        filter.setNodeId(0);
        filter.setArchive(false);
        filter.setRetries(0);
        filter.setRetryInterval(0);
        filter.setOnlyFaultyMessages(false);
        filter.setTimesFailed(0);
        filter.setWasEdited(false);
        
        request.setFilter(filter);
        //GetMessageListResponse response =(GetMessageListResponse) soapConnector.callWebService("http://localhost:50000/AdapterMessageMonitoring/basic?style=document", request);
        GetMessageListResponse response =(GetMessageListResponse) soapConnector.callWebService(url, request,username,password);
        System.out.println("sender interface:===="+receiverInterface);
		System.out.println("Got Response As below ========= : ");
        List<AdapterFrameworkData> data = response.getResponse().getList().getValue().getAdapterFrameworkData();
        
        for(AdapterFrameworkData msg:data) {
        	System.out.println("MesaageKey"+msg.getMessageKey().getValue());
        	System.out.println("MessageIdValue"+msg.getMessageID().getValue());
        	System.out.println("Message"+msg.getSenderInterface().getValue());
        	System.out.println("MessageVersion"+msg.getVersion().getValue());
        	Message m = new Message();
        	m.setMessageID(msg.getMessageID().getValue());
        	m.setMessageKey(msg.getMessageKey().getValue());
        	m.setSize(msg.getSize().getValue());
        	//m.setParentID(msg.getParentID().getValue());
        	
        	System.out.println(m.getMessageKey());
        	//TODO 
        	//m.setStartTime(msg.getStartTime().getValue().get);
        	m.setStatus(msg.getStatus().getValue());    	
        	messages.add(m);
    	}
        return messages;        
    }   
}