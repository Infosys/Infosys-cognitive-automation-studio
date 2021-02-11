/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot;


import java.io.IOException;
import java.net.ConnectException;
import java.net.HttpURLConnection;
import java.net.URISyntaxException;
import java.net.URL;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "VerifyUrl", version = "1.0", description = "", botCategory = "Url", author = "", technology = "Java", technologyCode = "01", botCategoryCode = "10", botId = "02")
public class VerifyUrl {
	private static final Logger log = LoggerFactory.getLogger(VerifyUrl.class);

	@Errors(exceptions = {
			@Error(errorCode = "01100211FF", errorMessagePattern = ".*", exceptionClass = IOException.class)
	})
	public Status execute(
			@InputParameter(name = "UrlString") String urlString,
			@OutputParameter(name = "Response") ObjectHolder<String> response)
					throws ExecutionError,IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA;
		String errorCodeB;
		String errorDescrption;
		if(urlString.equals(null))
		{
			errorCodeA="1";
			errorCategoryCode = "1";
			errorCodeB = "0D";
			errorDescrption = "Invalid Url";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + urlString);
		}
		try{
			
			getconnectionstatus(urlString);
			response.setValue("Yes");
			return new Status("00", "Url is up and running");
		}
		catch(Exception e){
			response.setValue("No");
			return new Status("01100211FF",e.getMessage());
		}
		


	}

	public static  void  getconnectionstatus(String urlString) throws IOException {
		URL u = new URL(urlString); 
		HttpURLConnection huc =  (HttpURLConnection)  u.openConnection(); 
		huc.setRequestMethod("GET"); 
		huc.connect();
		
	}


}

