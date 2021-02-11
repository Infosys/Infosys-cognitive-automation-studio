/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.file;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*; 
import javax.mail.*; 
import javax.mail.internet.*; 
import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "SendEmailsUsingSMTP", version = "1.0", description = "", botCategory = "Outlook", author = "", technology = "Java", technologyCode = "01", botCategoryCode = "24", botId = "01")
public class SendEmailsUsingSMTP {
	private static final Logger log = LoggerFactory.getLogger(SendEmailsUsingSMTP.class);
	@Errors(exceptions= {
			@Error(errorCode="01240111FF", errorMessagePattern =".*" , exceptionClass=IOException.class),
			@Error(errorCode="0124011111", errorMessagePattern ="Field value NULL", exceptionClass = IOException.class)
		})

	public Status execute(
			@InputParameter(name="Recipient") String recipient,
			@InputParameter(name="Username") String username,
			@InputParameter(name="Password") String password,
			@InputParameter(name="Host") String host,
			@InputParameter(name="Subject") String subject,
			@InputParameter(name="MailBody") String body
			) throws ExecutionError, IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA = "1";
		String errorCodeB;
		String errorDescrption;
		
		if (recipient==null) {
			errorCategoryCode = "1";
			errorCodeB = "11";
			errorDescrption = "Field value NULL";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + recipient);
		}
		if (username==null) {
			errorCategoryCode = "1";
			errorCodeB = "11";
			errorDescrption = "Field value NULL";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + recipient);
		}
		if (password==null) {
			errorCategoryCode = "1";
			errorCodeB = "11";
			errorDescrption = "Field value NULL";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + recipient);
		}
		if (host==null) {
			errorCategoryCode = "1";
			errorCodeB = "11";
			errorDescrption = "Field value NULL";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + recipient);
		}
		
		try {
			Properties properties = System.getProperties();
			properties.put("mail.smtp.auth", "true");
			properties.put("mail.smtp.starttls.enable", "true");
			properties.put("mail.smtp.ssl.trust", host);
			properties.put("mail.smtp.host", host);
			properties.put("mail.smtp.port", "587");
			Session session = Session.getDefaultInstance(properties, new Authenticator() {
				@Override
				protected PasswordAuthentication getPasswordAuthentication() {
					return new PasswordAuthentication(username,password);
				}
			});
			MimeMessage message = new MimeMessage(session);
			message.setFrom(new InternetAddress(username));
			message.addRecipient(Message.RecipientType.TO,new InternetAddress(recipient));
			message.setSubject(subject);
			message.setText(body);
			message.saveChanges();
	        Transport transport = session.getTransport("smtp");
	        transport.connect(host,username,password);
	        transport.sendMessage(message,message.getAllRecipients());
			transport.close();
			log.info("Mail has been sent successfully");
			return new Status("00", "Mail has been sent successfully");
		}
		catch(Exception e){
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className );
			return new Status("Error",e.getMessage(),e);
		}
	}
}