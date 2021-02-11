/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.filemodification;

import java.io.FileWriter;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

//*****************************************************
//Input : Content of file, string to search and content that is to be put before search string.
//Output : The content is added before search string and is written in the output file.
//Description :  It reads the content of the file, searches the string and add the new content before the search string 
//The output is written into the file.
//*****************************************************

public class BeforeString implements JavaDelegate {
private static final Logger log = LoggerFactory.getLogger(BeforeString.class);
	
	public void execute(DelegateExecution execution) throws Exception {
		
		log.debug("*************** BeforeString ***********************");	
		String content = (String) execution.getVariable("Content");
		String stringPattern = (String) execution.getVariable("StringPattern");
		String newValue = (String) execution.getVariable("NewValue");
		String file = (String) execution.getVariable("File");
		log.debug("*** Before String conent is :"+content+"\n stringPattern :: "+stringPattern+"\n newValue ::"+newValue);
		String newValueString=newValue+" "+stringPattern;
		String beforeStringContent = content.replaceAll(stringPattern, "" + newValueString);
		log.debug("Before String test  ::"+beforeStringContent);
		FileWriter fw = new FileWriter(file);
		fw.write(beforeStringContent);
		fw.close();
	}
	
}
