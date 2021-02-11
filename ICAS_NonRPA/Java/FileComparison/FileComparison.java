/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.comparison;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.microbots.comparison.filecomparisontool.Comparator;
import com.infosys.impact.botfactory.microbots.comparison.filecomparisontool.FileComparatorTool;
import com.infosys.impact.botfactory.microbots.comparison.xmlcomparator.XMLComparator;
import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.infosys.impact.botfactory.microbots.framework.Validation;
import com.infosys.impact.botfactory.microbots.comparison.Report;

import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;
import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.NON_EMPTY;

import java.io.IOException;
import java.io.Serializable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
@Bot(name = "FileComparison", version = "1.0", description = "", botCategory = "Comparison", author = "", technology = "Java", 
technologyCode = "01", botCategoryCode = "18", botId = "02")
public class FileComparison implements Serializable{
	private static final Logger log = LoggerFactory.getLogger(FileComparison.class);
	@Errors(exceptions= {
			@Error(errorCode = "01180911FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
		})
	
	public Status execute(
			@InputParameter(name = "OriginalFile") String originalFile,
			@InputParameter(name = "UpdatedFile") String updatedFile,
			@InputParameter(name = "ElementPathInOriginalFile", required = false) String elementPathInOriginalFile,
			@InputParameter(name = "ElementPathInUpdatedFile", required = false) String elementPathInUpdatedFile,
			@InputParameter(name = "ComparisonType") String comparisonType,
			@InputParameter(name = "Report") Report report)throws ExecutionError, IOException{
				try {
			Comparator comparator = null;
			System.out.println("Before FileComparisonStep.execute()");
			/*
			 * if ((bean.getParameterByName("comparisonType").getValue().toString()).
			 * equals("Line By Line Comparison")) { comparator = new FileComparatorTool(); }
			 * else if ((bean.getParameterByName("comparisonType").getValue().toString()).
			 * equals("XML Comparison")) { comparator = new XMLComparator(); }
			 */
			if (comparisonType.equals("Line By Line Comparison")) {
				comparator = new FileComparatorTool();
			} else if (comparisonType.equals("XML Comparison")) {
				comparator = new XMLComparator();
			} else {
				report.addEntry(new ReportEntry("Error", this, "Invalid comparisonType"+comparisonType));				
			}
			report.getClass();
			System.out.println("++++++++++++++++++++++++++++++"+report.getClass());
			Table table = comparator.compare(Utility.readFile(originalFile), Utility.readFile(updatedFile),
					elementPathInOriginalFile, elementPathInUpdatedFile);
			report.addEntry(new ReportEntry("Success","FileComparisonBot" , table));
			//updateAllListeners(100, "Completed comparison", new Object[]{});
			//finalReport.setValue(report);
			System.out.println("FileComparisonStep.execute().. returning");
			return new Status("0000000000", "Compared Test Report successfully ");
		} catch (Exception e) {
			report.addEntry(new ReportEntry("Error", this, "" + e.getMessage() + "\n" + Utility.getStackTrace(e)));
			return new Status("Error",e.getMessage(),e);
		}
		
	}

}
