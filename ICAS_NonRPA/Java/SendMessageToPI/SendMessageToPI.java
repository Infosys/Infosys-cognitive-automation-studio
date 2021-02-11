/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.sap_pi;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.URL;
import java.text.DecimalFormat;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;
import java.util.Random;

import javax.activation.DataHandler;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.soap.AttachmentPart;
import javax.xml.soap.MessageFactory;
import javax.xml.soap.SOAPConnection;
import javax.xml.soap.SOAPConnectionFactory;
import javax.xml.soap.SOAPElement;
import javax.xml.soap.SOAPException;
import javax.xml.soap.SOAPMessage;
import javax.xml.soap.SOAPPart;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.apache.commons.codec.binary.Base64;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "SendMessageToPI", version = "1.0", description = "", botCategory = "SAP", author = "", technology = "Java", 
technologyCode = "01", botCategoryCode = "0C", botId = "04")
public class SendMessageToPI{
	private static final Logger log = LoggerFactory.getLogger(SendMessageToPI.class);
	 @Errors(exceptions= {
				@Error(errorCode = "010C0411FF", errorMessagePattern = ".*", exceptionClass = IOException.class)
		})
	    public Status execute(
				//@InputParameter(name = "PIServer") String piServer,
				//@InputParameter(name = "InterfaceID") String interfaceID
				@InputParameter(name = "Payload") byte[] payload,
				@InputParameter(name = "SOAPUrl")String SOAPUrl,
				@InputParameter(name = "service")String service, 
				@InputParameter(name = "namespace")String namespace, 
				@InputParameter(name = "Interface")String Interface,
				@InputParameter(name = "creds")String creds,
				@OutputParameter(name = "MessageID") ObjectHolder<String> messageID
				)throws ExecutionError,IOException {
		 try {	
			 
			 String messageId = sendSOAPMessage(payload,SOAPUrl,service,namespace,Interface,creds);
			 messageID.setValue(messageId);	
			 return new Status("00","Payload Sent to server");
		} catch (UnsupportedOperationException | XPathExpressionException | SOAPException | IOException
				| ParserConfigurationException | SAXException | TransformerFactoryConfigurationError
				| TransformerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return new Status("Error",e.getMessage(),e);
		}
		 
		
	 }
	/*public static void main(String[] args) {
		 try {
			
			new SendMessageToPI().sendSOAPMessage(readFile("D:\\Code\\Impact\\Demo\\f748e3fc-0ab8-2d1d-00d6-558575716e7d.txt").getBytes());
			
		} catch (UnsupportedOperationException | XPathExpressionException | SOAPException | IOException
				| ParserConfigurationException | SAXException | TransformerFactoryConfigurationError
				| TransformerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}*/
	
	public String sendSOAPMessage(byte[] payload, String SOAPUrl,String service, String namespace, String Interface,String creds) throws SOAPException, FileNotFoundException, IOException, UnsupportedOperationException, ParserConfigurationException, SAXException, TransformerFactoryConfigurationError, TransformerException, XPathExpressionException {
		String strResponse = null;
		//InitTestCaseProperties testcaseProperties = InitTestCaseProperties.getInstance();
		//String SOAPUrl = "http://brsdhtcsaph1:50000/XISOAPAdapter/MessageServlet?channel=:BC_INF622534_BPM_N74:CC_INF622534_BPM_N74_SOAPXI_Sender";
		//brsdhtcsaph1
		System.out.println("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"+SOAPUrl);
		InputStream fin = null;
		//fin = new FileInputStream("SOAPTEMPLATE.xml");
		//fin=SendMessageToPI.class.getResourceAsStream("SOAPTEMPLATE.xml")	;
		fin = SendMessageToPI.class.getClassLoader().getResourceAsStream("config/SOAPTEMPLATE.xml");

		//fin = new FileInputStream(xmlFilePath);
		Properties properties=new Properties();
		//TODO Populate properties with header data
//		System.out.println("SenderParty:: = "+inf.getSenderParty());
//		System.out.println("SenderService:: ="+inf.getSenderComponent());
//		System.out.println("SenderService:: ="+inf.getSenderNamespace());
//		System.out.println("SenderService:: ="+inf.getSenderInterface());
		//if(inf.getSenderParty()!=null && !inf.getSenderParty().equals("")){
			//properties.setProperty("//Sender/Party", inf.getSenderParty());
			/*properties.setProperty("//Sender/Party/@agency", "http://sap.com/xi/XI");
			properties.setProperty("//Sender/Party/scheme", "XIParty");*/
		//}
		//properties.setProperty("//Sender/Service", "BC_INF763251_FTF_Sender");
		//properties.setProperty("//Main/Interface/@namespace", "http://infosys.com/pi/INF763251");
		//properties.setProperty("//Main/Interface", "SI_INF763251_FTF1_Sender");
		
		properties.setProperty("//Sender/Service", service);
		properties.setProperty("//Main/Interface/@namespace", namespace);
		properties.setProperty("//Main/Interface", Interface);
		
		byte[] b = getData(fin, properties); 
		System.out.println("Byte Content "+new String(b));
		
		
		ByteArrayInputStream bis = new ByteArrayInputStream(b);
		StreamSource ssrc = new StreamSource(bis);

		SOAPConnectionFactory factory = null;
		factory = SOAPConnectionFactory.newInstance();
		SOAPConnection connection = null;
		connection = factory.createConnection();
		MessageFactory messageFactory = MessageFactory.newInstance();
		javax.xml.soap.SOAPMessage message = messageFactory.createMessage();
		
		SOAPPart soapPart = message.getSOAPPart();
		soapPart.setContent(ssrc);
		//String creds = "INF29224:Raj@n74";
		//String creds = creds;
		message.getMimeHeaders().addHeader("Authorization", "Basic " + new String(Base64.encodeBase64(creds.getBytes())));

		UniqueKeyGenerator ukgObj = new UniqueKeyGenerator();
		String messageId = ukgObj.getUUID();
 
		String id = "payload-f21a0e41186a11am99de000e0c60" + new DecimalFormat("####").format(new Random().nextInt(10000)) + "@sap.com";
		Element payloadNode = (Element) message.getSOAPBody().getElementsByTagName("SAP:Payload").item(0);
		String current = payloadNode.getAttributes().getNamedItem("xlink:href").getNodeValue();
		System.out.println(current);
		payloadNode.setAttribute("xlink:href", "cid:" + id);
		DataHandler handler = null;
//		if(inf.getSenderNamespace().equals("urn:sap-com:document:sap:idoc:messages")){
//			//String fileContent = Utility.read(payloadFileName);
//			handler = new DataHandler(new StreamSource(new ByteArrayInputStream(ChangeIDocControlRecord.changeControlRecord(new File(payloadFileName),controlRecordProperties ))), "text/xml");
//			//handler = new DataHandler(new StreamSource(new FileInputStream(ChangeIDocControlRecord.changeControlRecord(fileContent,controlRecordProperties ))), "text/xml");
//		}else{
		    //new InputSource(new InputStreamReader(inputStream))
		    handler = new DataHandler(new StreamSource(new InputStreamReader(new ByteArrayInputStream(payload))), "text/xml");
		    //handler = new DataHandler(new InputSource(new InputStreamReader(new FileInputStream(payloadFileName))), "text/xml");
//		}
		//handler = new DataHandler(new StreamSource(new FileInputStream(payloadFileName)), "text/xml");
		AttachmentPart attachPart = message.createAttachmentPart(handler);
		attachPart.setContentType("text/xml");

		attachPart.setContentId(id);
		message.addAttachmentPart(attachPart);
		SOAPMessage reply = null;
		Iterator it = null;
		it = message.getSOAPHeader().getChildElements();
		int headerCount = 0;
		while (it.hasNext()) {

			headerCount++;
			Object obj = it.next();
			if (obj instanceof SOAPElement) {
				SOAPElement se = ((SOAPElement) obj);
				Iterator it1 = se.getChildElements();
				while (it1.hasNext()) {
					Node node = ((Node) it1.next());
					if (node.getNodeName().equals("SAP:MessageId")) {
						node.getChildNodes().item(0).setNodeValue(messageId);
					}

				}
			}
		}
		System.out.println("Message++++"+message);
		reply = connection.call(message, new URL(SOAPUrl));
		
		ByteArrayOutputStream bos = new ByteArrayOutputStream();
		if(reply!=null){
			reply.writeTo(bos);
			strResponse = bos.toString("UTF-8");
			System.out.println("\n retstring is " + strResponse);
			if(strResponse.contains("<SOAP:Fault")){
			messageId = "Error: No Message ID";
			if(strResponse.contains("<SAP:Stack>")){
				messageId = messageId+strResponse.substring(strResponse.indexOf("<SAP:Stack>"),strResponse.indexOf("</SAP:Stack>"));
			}
			}
		}
		bis.close();
		bos.close();
		fin.close();
		return messageId;
	}
	public static void copy(InputStream in, OutputStream out) throws IOException {

		// do not allow other threads to read from the
		// input or write to the output while copying is
		// taking place

		synchronized (in) {
			synchronized (out) {

				byte[] buffer = new byte[256];
				while (true) {
					int bytesRead = in.read(buffer);
					if (bytesRead == -1)
						break;
					out.write(buffer, 0, bytesRead);
				}
			}
		}
	}

	public static String readFile(String fileName) throws IOException {
		FileInputStream fileInputStream = new FileInputStream(fileName);
		byte[] bs = new byte[fileInputStream.available()];
		fileInputStream.read(bs);
		return new String(bs);
	}
	private String getTextValue(Element ele, String tagName) {
		String textVal = null;
		NodeList nl = ele.getElementsByTagName(tagName);
		if (nl != null && nl.getLength() > 0) {
			Element el = (Element) nl.item(0);
			textVal = el.getFirstChild().getNodeValue();
		}
		return textVal;
	}
	private static byte[] getData(InputStream inputStream, Properties properties) throws ParserConfigurationException, SAXException, IOException, TransformerFactoryConfigurationError, TransformerException, XPathExpressionException{
		ByteArrayOutputStream bout = new ByteArrayOutputStream();
		DocumentBuilderFactory builderFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = builderFactory.newDocumentBuilder();
		Document document = builder.parse(inputStream);
		XPathFactory xPathFactory=XPathFactory.newInstance();
		XPath xPath=xPathFactory.newXPath();
		
		for(Object key:properties.keySet()){
			Node node=(Node) xPath.evaluate(key.toString(), document,XPathConstants.NODE);
			if(node.getNodeType()==Node.ATTRIBUTE_NODE){
				node.setNodeValue(properties.getProperty((String) key));	
			}else{
				node.setTextContent(properties.getProperty((String) key));
			}			
		}		
		Transformer transformer = TransformerFactory.newInstance().newTransformer();
		transformer.transform(new DOMSource(document), new StreamResult(bout));
		inputStream.close();
		return bout.toByteArray();
	}
}
