/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.comparison;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Date;


import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Templates;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "ReportBot", version = "1.0", description = "", botCategory = "Report", author = "", technology = "Java", 
technologyCode = "01", botCategoryCode = "26", botId = "01")
public class ReportBot {
	/**
	 * <code>Logger</code> object used to log all log messages related to <code>TestReportTask</code> class
	 */
	//private static final Logger log =(Logger) LoggerFactory.getLogger(ReportBot.class);
	private static final Logger log = LoggerFactory.getLogger(ReportBot.class);
	@Errors(exceptions= {
			@Error(errorCode = "01260111FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
		})
	public Status execute(@InputParameter(name="Report") Report report,
			@InputParameter(name="FolderPath") String folderPath,
			@InputParameter(name="XmlFileName") String xmlFileName,
			@InputParameter(name="HtmlFileName") String htmlFileName,
			@InputParameter(name="TestPlanName") String testPlanName,
			@OutputParameter(name="ReportFilePath") ObjectHolder<String> reportfilePath)
			throws IOException,ExecutionError {
		try{
			//logger.info("Starting with reporting");
			Report r = new Report();
			r=report;
			r.setStatus("Success");
			r.setEndTime(new Date());
			String xmlReport=new XMLConverter().serialize(r);
			//logger.fine("TestReportTask.execute()\n"+xmlReport);
			
			//File outputDir=r.getOutputDir(); 
			//File outputDir=new File("D:\\Report");
			File outputDir=new File(folderPath);
			outputDir.mkdirs();
			//String cssContent=Utility.read(this.getClass().getClassLoader().getResourceAsStream("reporting/TestReport.css"));
			//Utility.write(new File(outputDir,"TestReport.css").getPath(),cssContent);
			
			Utility.write(new File(outputDir,xmlFileName+System.currentTimeMillis()+".xml").getPath(),xmlReport);
			System.out.println("XML REPORT"+xmlReport);
			StreamSource source = new StreamSource(new ByteArrayInputStream(xmlReport.getBytes()));
			//log.info("Going to test TestReport.xsl");
			StreamSource testreport = new StreamSource(this.getClass().getClassLoader().getResourceAsStream("reporting/TestReport1.xsl"));
			System.out.println("FInd the testreport"+testreport);
			
			TransformerFactory factory = TransformerFactory.newInstance();
			Templates templates = factory.newTemplates(testreport);
			Transformer dtdx2flatTransformer = templates.newTransformer();
			r.setTestPlanName(testPlanName);
			File htmlReport=new File(outputDir,htmlFileName+"_"+r.getTestPlanName()+"_"+System.currentTimeMillis()+".html");
			r.setSummaryFileName("Summary");
			System.out.println("<<<<<<<<<<<<<<<<<SummaryFileName        "+r.getSummaryFileName());
		
			//htmlReport1=new File(r.getSummaryFileName());
			FileOutputStream os=new FileOutputStream(htmlReport);
			StreamResult result = new StreamResult(os);
			dtdx2flatTransformer.transform(source, result);
			System.out.println("Finally Complete");
			reportfilePath.setValue(htmlReport.getPath());
			return new Status("0000000000","Report generated successfully");
		}catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}

	}
}
