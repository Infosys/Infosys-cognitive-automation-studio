/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.file;
import java.io.IOException;
//import java.util.ArrayList;
//import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
//import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
//import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.sun.jna.platform.win32.Advapi32Util.EventLogIterator;
import com.sun.jna.platform.win32.Advapi32Util.EventLogRecord;

@Bot(name = "ReadWindowsEventLogs", version = "1.0", description = "", botCategory = "System", author = "",technology = "", technologyCode = "01", botCategoryCode = "28", botId = "01")

public class ReadWindowsEventLogs {
	private static final Logger log = LoggerFactory.getLogger(ReadWindowsEventLogs.class);
	@Errors(exceptions= {
			@Error(errorCode="01280111FF", errorMessagePattern =".*" , exceptionClass=IOException.class),
			@Error(errorCode="0128011111", errorMessagePattern ="Field value NULL", exceptionClass = IOException.class)
		})

	public Status execute(
			@InputParameter(name="Type") String type
//			@OutputParameter(name ="EventLog") ObjectHolder<List<String>> eventLog
			) throws ExecutionError, IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA = "1";
		String errorCodeB;
		String errorDescrption;

		if (type==null) {
			errorCategoryCode = "1";
			errorCodeB = "11";
			errorDescrption = "Field value NULL";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + type);
		}
		
		log.info("Starting process....");

		try {
			EventLogIterator iter = new EventLogIterator(type);
//			List<String> event = new ArrayList<>();
			while(iter.hasNext()) { 
			    EventLogRecord record = iter.next(); 
			    log.info(record.getRecordNumber() 
			            + ": Event ID: " + record.getEventId() 
			            + ", Event Type: " + record.getType() 
			            + ", Event Source: " + record.getSource()); 
			}
//			eventLog.setValue(event);
			return new Status("00", "Event log of type "+type+" has been recorded successfully.");
		}
		catch(Exception e){
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className );
			return new Status("Error",e.getMessage(),e);
		}
	}
}