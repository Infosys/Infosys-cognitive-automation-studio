/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbot.file;

import java.io.*;
import org.apache.poi.xwpf.extractor.XWPFWordExtractor;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FILE;
import java.io.File;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "ConvertWordToText", version = "1.0", description = "", botCategory = "File", author = "", technology = "Java", technologyCode = "01", botCategoryCode = "01", botId = "11")

public class ConvertWordToText {
	private static final Logger log = LoggerFactory.getLogger(ConvertWordToText.class);

	@Errors(exceptions = {
			@Error(errorCode = "01011411FF", errorMessagePattern = ".*", exceptionClass = IOException.class),
			@Error(errorCode = "0101141103", errorMessagePattern = "File Does Not Exist", exceptionClass = IOException.class) })

	public Status execute(@InputParameter(name = "WordFilePath", constraints = { EXISTS, FILE }) String wordFilePath,
			@InputParameter(name = "TextFilePath", constraints = { EXISTS, FILE }) String textFilePath) throws ExecutionError, IOException {
		String botErrorCode;
		String errorCategoryCode;
		String errorCodeA;
		String errorCodeB;
		String errorDescrption;

		if (wordFilePath.equals(null)) {
			errorCodeA = "1";
			errorCategoryCode = "1";
			errorCodeB = "03";
			errorDescrption = "File Does Not Exist";
			botErrorCode = errorCategoryCode + errorCodeA + errorCodeB;
			throw new ExecutionError(botErrorCode, errorDescrption + wordFilePath);
		}

		File file = null;

		try {
			// Read the Doc/DOCx file
			file = new File(wordFilePath);
			FileInputStream fis = new FileInputStream(file.getAbsolutePath());
			XWPFDocument doc = new XWPFDocument(fis);
			XWPFWordExtractor ex = new XWPFWordExtractor(doc);
			String text = ex.getText();

			// write the text in txt file
			File txtFile = new File(textFilePath);
			Writer output = new BufferedWriter(new FileWriter(txtFile));
			output.write(text);
			output.close();
			ex.close();
			System.out.println("Converted word to text successfully");
			log.info("Converted word to text successfully........");
			return new Status("00", "Converted word to text successfully");
		} catch (Exception e) {
			String className = this.getClass().getSimpleName();
			log.info("Display Error code ::" + className);
			return new Status("Error", e.getMessage(), e);
		}
	}
}
