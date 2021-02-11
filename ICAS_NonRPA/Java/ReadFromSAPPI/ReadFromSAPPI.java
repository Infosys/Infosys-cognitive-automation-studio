/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.sap.pi;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "ReadFromSAPPI", version = "1.0", description = "", botCategory = "SAP", author = "", technology = "Java", 
technologyCode = "01", botCategoryCode = "01", botId = "01")
public class ReadFromSAPPI {
	
	public Status execute(
			@InputParameter(name = "PIServer") String PIServer,
			@InputParameter(name = "InterfaceID") String interfaceID,
			@InputParameter(name = "Version") String payload,
			@OutputParameter(name = "RawPayload") ObjectHolder<String> rawPayload
			) {
		try {
			System.out.println("ReadFromSAPPI.execute().. ");
			rawPayload.setValue("RAW_PAY_LOAD");
			
		} catch (Exception e) {
			
		}
		return new Status("0000000000", "Compared Test Report successfully ");
	}

}
