/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.sap_pi;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.xml.bind.JAXBElement;
import javax.xml.namespace.QName;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.oxm.jaxb.Jaxb2Marshaller;

import com.infosys.impact.botfactory.custom.table.Table;
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
import com.infosys.impact.botfactory.microbots.sap_pi.gen.GetMessageBytesJavaLangStringIntBoolean;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.GetMessageBytesJavaLangStringIntBooleanResponse;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.GetMessageList;
import com.infosys.impact.botfactory.microbots.sap_pi.gen.GetMessageListResponse;

@Bot(name = "GetMessagePayloadFromSAPPI", version = "1.0", description = "", botCategory = "SAP", author = "", technology = "Java",
technologyCode = "01", botCategoryCode = "0C", botId = "02")
public class GetMessagePayloadFromSAPPI {
	private static final Logger log = LoggerFactory.getLogger(GetMessagePayloadFromSAPPI.class);
    public static void main(String[] args) {
    	GetMessagePayloadFromSAPPI getMessagePayload= new GetMessagePayloadFromSAPPI();
    	String messageKey = "33397cba-0a25-0a39-162b-6cfd959c0129\\OUTBOUND\\5694050\\EO\\0\\";
    	//messageKey.split("\\");
    	Jaxb2Marshaller marshaller= new Jaxb2Marshaller();
    	marshaller.setContextPath("com.infosys.impact.botfactory.microbots.sap_pi.gen");
    	String url="http://brsdhtcsaph1:50000/AdapterMessageMonitoring/basic?style=document";
    	SOAPConnector soapConnector = getMessagePayload.soapConnector(marshaller,url);
    	String username="inf1037562";
    	String password="Anish@27";
    	byte[] messages = getMessagePayload.lookup(soapConnector,messageKey,"4",url,username,password);
    	System.out.println(new String(messages));
    	messages = getMessagePayload.lookup(soapConnector,messageKey,"4",url,username,password);
    	System.out.println("---------------------------------------------------------------\n"+new String(messages)+"\n---------------------------------------------------------------");
    }

    @Errors(exceptions= {
			@Error(errorCode = "010C0211FF", errorMessagePattern = ".*", exceptionClass = IOException.class)
	})
    public Status execute(
			@InputParameter(name = "MessageKey") String messageKey,
			@InputParameter(name = "Version") String version,
			@InputParameter(name = "Url") String url,
			@InputParameter(name = "Username") String username,
			@InputParameter(name = "Password") String password,
			@OutputParameter(name = "MessagePayload") ObjectHolder<byte[]> messagePayload
			)throws ExecutionError,IOException {
    	try {
    	Jaxb2Marshaller marshaller= new Jaxb2Marshaller();
    	marshaller.setContextPath("com.infosys.impact.botfactory.microbots.sap_pi.gen");
		//marshaller.setContextPath(contextPath);
    	System.out.println("MessageKeyforGetMessagePayloadFromSAPPI "+messageKey);
    	SOAPConnector soapConnector = soapConnector(marshaller,url);
    	byte[] messageBytes = lookup(soapConnector,messageKey,version,url,username,password);
    	System.out.println();
    	messagePayload.setValue(messageBytes);
    	//System.out.println("MessageList"+messageList);
    	
    	return new Status("00","Created a list of maps");}
    	catch(Exception e){
			
    		return new Status("Error",e.getMessage(),e);
    	}
    }

    public SOAPConnector soapConnector(Jaxb2Marshaller marshaller, String url) {
        SOAPConnector client = new SOAPConnector();
        //client.setDefaultUri("http://brsdhtcsaph1:50000/AdapterMessageMonitoring/basic?style=document");
		client.setDefaultUri(url);
        client.setMarshaller(marshaller);
        client.setUnmarshaller(marshaller);
        return client;
    }
    private byte[] lookup(SOAPConnector soapConnector,String messageKey,String version, String url,String username, String password ) {
        GetMessageBytesJavaLangStringIntBoolean request = new GetMessageBytesJavaLangStringIntBoolean();
        request.setMessageKey(messageKey);
        request.setVersion(Integer.parseInt(version));
        //GetMessageBytesJavaLangStringIntBooleanResponse response =(GetMessageBytesJavaLangStringIntBooleanResponse) soapConnector.callWebService("http://brsdhtcsaph1:50000/AdapterMessageMonitoring/basic?style=document", request);
        GetMessageBytesJavaLangStringIntBooleanResponse response =(GetMessageBytesJavaLangStringIntBooleanResponse) soapConnector.callWebService(url, request,username,password);
		System.out.println("Got Response As below ========= : ");
        byte[] data = response.getResponse();
        return data;
    }
}