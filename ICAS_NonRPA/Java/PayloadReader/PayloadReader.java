/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.sap_pi;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

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

@Bot(name = "PayloadReader", version = "1.0", description = "", botCategory = "SAP", author = "", technology = "Java", technologyCode = "01", botCategoryCode = "0C", botId = "03")
public class PayloadReader {
	private static final Logger log = LoggerFactory.getLogger(PayloadReader.class);
	 @Errors(exceptions= {
				@Error(errorCode = "010C0311FF", errorMessagePattern = ".*", exceptionClass = IOException.class)})
	public Status execute(@InputParameter(name = "InputPayload", required = false) byte[] payload,
			@OutputParameter(name = "OutputPayload") ObjectHolder<byte[]> outputPayload) throws ExecutionError,IOException{
		StringBuffer sb = new StringBuffer();
		int linecount = 0;
		int invalidlines = 0;
		InputStream is = null;
		BufferedReader br = null;
		System.out.println("<<Payload:>>");
		if(payload==null) {
			//log.info("No content available. Ignoring file");
			return new Status("01", "No content available. Ignoring file");
		}
		try {
			is = new ByteArrayInputStream(payload);
			br = new BufferedReader(new InputStreamReader(is));
			String data;
			while ((data = br.readLine()) != null) {
				linecount++;
				if ((!data.startsWith("content-type:")) && (!data.startsWith("content-length:"))
						&& (!data.startsWith("--SAP_")) && (!data.startsWith("Content-ID:"))
						&& (!data.startsWith("content-id:")) && (!data.startsWith("Content-Type:"))
						&& (!data.startsWith("Content-Length:")) && (!data.startsWith("content-description:"))
						&& (!data.startsWith("Content-Disposition:")) && (!data.startsWith("Content-Description:"))
						&& (!data.startsWith("<SOAP:Envelope xmlns:SOAP")) && (!data.startsWith("--SAP_"))
						&& (!data.startsWith("http:POST")) && (!data.startsWith("HTTP:POST"))
						&& (!data.startsWith("sap-xi-length:")) && (!data.startsWith("host:"))
						&& (!data.startsWith("soapaction:")) && (!data.startsWith("user-agent:"))
						&& (!data.startsWith("accept-encoding:")) && (!data.startsWith("sap-xi-messageid:"))
						&& (!data.trim().equals(""))) {
					sb = sb.append(data+"\n");
				} else {
					invalidlines++;
				}
			}
			is.close();
			br.close();
			System.out.println("Total No of Lines!!" + linecount);
			System.out.println("No of invalidLines!!" + invalidlines);
			System.out.println(" sb.toString()==" + sb.toString());
			outputPayload.setValue(sb.toString().getBytes());
			//System.out.println("<<completed>>");
			return new Status("0000000000", "Successfully extracted the payload");
		} catch (Exception e) {
			e.printStackTrace();
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);
		}
		
	}

	/*public static void main(String[] args) {
		PayloadReader payloadReader = new PayloadReader();
		File file = new File("D:\\Code\\21March\\RawPayload.txt");
		byte[] bytesArray = new byte[(int) file.length()];
		ObjectHolder<byte[]> out = new ObjectHolder<>();				
		try {
			FileInputStream fis = new FileInputStream(file);
			fis.read(bytesArray); // read file into bytes[]
			fis.close();
			payloadReader.execute(bytesArray, out);
		} catch (Exception e) {
			// TODO: handle exception
		}
	}*/
}
