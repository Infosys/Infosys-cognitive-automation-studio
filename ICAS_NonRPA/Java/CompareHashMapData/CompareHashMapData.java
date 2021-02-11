/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.excel;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
@Bot(name="CompareHashMapData",version="1.0",description="",botCategory="Map",author="", technology = "Java",
technologyCode="01",botCategoryCode="0F",botId="01") 


public class CompareHashMapData {
	private static final Logger log = LoggerFactory.getLogger(CompareHashMapData.class);
	@Errors(exceptions= {
			@Error(errorCode = "010F0111FF", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class),
			@Error(errorCode = "010F011115", errorMessagePattern = "Table Does Not Exist", exceptionClass = IOException.class),
		})
	public Status execute(
			@InputParameter(name="SourceData") Map<String, String> sourceData ,
			@InputParameter(name="TargetData") Map<String, String> targetData,
			@OutputParameter(name="FinalComparedData") ObjectHolder< Map<String,String>> finalcomparedData
			) throws ExecutionError, IOException {
		
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA;
		String errorCodeB;
		String errorDescrption;
		if(sourceData.values().isEmpty() ||targetData.values().isEmpty())
		{
			errorCodeA = "1";
			errorCategoryCode = "1";
			errorCodeB = "15";
			errorDescrption = "Table Does Not Exist";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + sourceData+targetData);
		}
		
		try {

			finalcomparedData.setValue(compareMap(sourceData,targetData));
			
			
			return new Status("00","Data Comparison Done ");
		} catch (Exception e) {
			
			String className = this.getClass().getSimpleName();
			return new Status("010F0111FF",e.getMessage());
		}

	
	}
	public static Map<String, String> compareMap(Map<String, String> excelData,Map<String, String> pdfData) {
		
		Map<String, String> finalData=new HashMap<String,String>();		
	    int count=0;
	    ArrayList<String> list=new ArrayList<String>();
		if (excelData == null || pdfData == null)
	        return null;
	    for (Map.Entry<String, String> entry : pdfData.entrySet()) {
	        String key = entry.getKey();
	        String tab = entry.getValue();
	        
	        for (Map.Entry<String, String> entry1 : excelData.entrySet()) {
		        String key1 = entry1.getKey();
		        String tab1 = entry1.getValue();
		        //System.out.println("Key"+key+"Value"+tab+"Key1"+key1+"Value1"+tab1);
		        if(key.equals(key1)) {
		        	if(tab.equals(tab1)) {
		        		finalData.put(key, tab);
		        		
		        	}
		        	else {
		        		count+=1;
		        		list.add(key);
		        		finalData.put(key, tab);		        		
		        	}
		        }        
	        }
	        }	    
	    if(count==0) {
	    	finalData.put("Validation","Success");
	    }
	    else
	    {
	    	finalData.put("Validation","Failed"+"("+list+")");
	    }
	   // System.out.println("finalData"+finalData);
	    return  finalData;   
	}
}
