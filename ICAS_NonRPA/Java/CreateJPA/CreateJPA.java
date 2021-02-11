/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.java;

/*
 * create JPA files as per database tables
 */
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class CreateJPA  {

	private static final Logger log = LoggerFactory.getLogger(CreateJPA.class);

	public Status execute(
			@InputParameter(name="Configuration") Properties conf,
			@InputParameter(name="TablesName") String tableName,
			@InputParameter(name="TargetPath") String targetPath,	
			@OutputParameter(name="TablesName") ObjectHolder<String> tableNameOut
			) throws Exception {

		try {
			String downloadedAssetsService = readFile(conf.getProperty("Templates.JPA"));

			targetPath += "\\src\\main\\java\\com\\infosys\\impact\\botorch\\repository\\";

			String[] className = tableName.split("\\|");
			for (int i = 0; i < className.length; i++) {
				String lcClassName = className[i].toLowerCase();

				String replacedtext = downloadedAssetsService.replaceAll("Student", "" + className[i]);
				replacedtext = replacedtext.replaceAll("student", "" + lcClassName);

				String targetDest = targetPath + "\\" + className[i] + "Repository.java";

				FileWriter writer = new FileWriter(targetDest);

				writer.write(replacedtext);

				writer.close();

			}
			
			tableNameOut.setValue(tableName);
			log.info("JPA created successfully at =" + targetPath);
			return new Status("00","JPA created successfully ");
		} catch (Exception e) {
			return new Status("Error",e.getMessage(),e);
		}

	}

	private static String readFile(String path) throws IOException {
		System.out.println(path);
		BufferedReader reader = new BufferedReader(new FileReader(path));
		StringBuffer sb = new StringBuffer();
		String l = null;
		do {
			l = reader.readLine();
			if (l != null) {
				sb.append(l + "\n");
			}
		} while (l != null);
		reader.close();
		return sb.toString();
	}

}
