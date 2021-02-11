/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.net.URI;
import java.net.URL;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

 

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

 

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

import microsoft.exchange.webservices.data.autodiscover.IAutodiscoverRedirectionUrl;
import microsoft.exchange.webservices.data.core.ExchangeService;
import microsoft.exchange.webservices.data.core.enumeration.misc.ExchangeVersion;
import microsoft.exchange.webservices.data.core.service.item.EmailMessage;
import microsoft.exchange.webservices.data.credential.ExchangeCredentials;
import microsoft.exchange.webservices.data.credential.WebCredentials;
import microsoft.exchange.webservices.data.property.complex.MessageBody;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;

@Bot(name = "SendMailUsingEWS", version = "1.0", description = "", botCategory = "Email", author = "", 
technology = "", technologyCode = "01", botCategoryCode = "1D", botId = "03")
public class SendMailUsingEWS{
	@Errors(exceptions= {
			@Error(errorCode = "011D0111FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			
		})
	private static final Logger log = LoggerFactory.getLogger(SendMailUsingEWS.class);
	
	public void sendMail(String emailFrom,String password,String emailTo,String emailSubject,String emailBody) throws Exception {
       
	   
       
            ExchangeService service = new ExchangeService(ExchangeVersion.Exchange2010_SP2);
            ExchangeCredentials credentials = null;
			try{
				credentials=new WebCredentials(emailFrom, password);
			}
			catch(Exception e){
				throw new Exception("Password is Wrong");
			}
            service.setCredentials(credentials);
            service.setUrl(new URI("https://outlook.office365.com/ews/exchange.asmx"));
//            service.autodiscoverUrl(emailFrom,new RedirectionUrlCallback());
           
       
        EmailMessage msg= new EmailMessage(service);
        msg.setSubject(emailSubject);
        msg.setBody(MessageBody.getMessageBodyFromText(emailBody));
//        BufferedInputStream in = new BufferedInputStream(new URL("https://test.com").openStream());
//        msg.getAttachments().addFileAttachment("tesct",in);
        msg.getToRecipients().add(emailTo);
        try {
            msg.sendAndSaveCopy();
        }
        catch (Exception e) {
           log.info("Exception Ocuured While Sending the Mail ");
            throw new Exception(e.getMessage());
//            e.printStackTrace();
        }
       
    }
	
	/*
	 * String emailFrom,String password,String emailTo, String mailBody
	 */
	public Status execute(    @InputParameter(name="emailFrom") String emailFrom,
            @InputParameter(name="password") String password,
            @InputParameter(name="emailTo") String emailTo,
          
			@InputParameter(name="emailBody") String emailBody,
			@InputParameter(name="emailSubject") String emailSubject
            ) throws ExecutionError {
		
				String botErrorCode;
				String errorCategoryCode;
				String errorCodeA;
				String errorCodeB;
				String errorDescrption;

			
                try {
                 
                	log.info("Email Body: "+emailBody);
                	log.info("EmailFrom: "+emailFrom);
                	log.info("EmailTo : "+emailTo);
                	log.info("EmailSubject: "+emailSubject);
                   
					if(!emailFrom.contains("@")){
						errorCodeA = "1";
						errorCategoryCode = "1";
						errorCodeB = "03";
						errorDescrption = "FROM Email is Wrong";
						botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
						throw new ExecutionError(botErrorCode, errorDescrption);
					}
					if(!emailTo.contains("@")){
						errorCodeA = "3";
						errorCategoryCode = "1";
						errorCodeB = "03";
						errorDescrption = "TO Email is Wrong";
						botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
						throw new ExecutionError(botErrorCode, errorDescrption);
					}
                    SendMailUsingEWS mailSender=new SendMailUsingEWS();
                    mailSender.sendMail(emailFrom, password, emailTo,emailSubject,emailBody);
                    return new Status("00","Mail Sent Successfully");
                }
                catch (Exception e) {
					if(e.getMessage().equals("Password is Wrong")){
						errorCategoryCode = "1";
						errorCodeA = "2";
						errorCodeB = "03";
						errorDescrption = "Password is Wrong";
						 botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
						throw new ExecutionError(botErrorCode, errorDescrption);
						
					}
                    return new Status("Error",e.getMessage(),e);
                }
    }


//	public static void main(String[] args) throws Exception {
//		MailSender mailSender =new MailSender();
//		String emailFrom="test@test.com";
//		String password="test$";
//		String emailTo="test@test.com";
//		String mailBody="Welcome";
//		try {
//			mailSender.sendMail(emailFrom, password, emailTo, mailBody);
//			System.out.println("Mail Sent");
//		}
//		catch (Exception e) {
//			System.out.println("Error Occuured ");
//			e.printStackTrace();
//			
//		}
//		
//	}
	
	static class RedirectionUrlCallback implements IAutodiscoverRedirectionUrl {
        public boolean autodiscoverRedirectionUrlValidationCallback(
                String redirectionUrl) {
            return redirectionUrl.toLowerCase().startsWith("https://");
        }
    }

}
