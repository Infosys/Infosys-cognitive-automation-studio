/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.comparison;

import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "InitiateReport", version = "1.0", description = "", botCategory = "Report", author = "",
technology = "Java", technologyCode = "01", botCategoryCode = "26", botId = "02")
public class InitiateReport {
	private static final Logger log = LoggerFactory.getLogger(InitiateReport.class);
	@Errors(exceptions= {
			@Error(errorCode = "01260211FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
		})
	public Status execute(
			@OutputParameter(name="Report") ObjectHolder<Report> report)throws ExecutionError{		
		report.setValue(new Report());
		return new Status("0000000000","Created Test Report");
	}
}
