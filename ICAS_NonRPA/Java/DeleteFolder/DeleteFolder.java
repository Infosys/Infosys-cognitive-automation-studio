/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.FOLDER;

/*
 * delete a folder 
 */
import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.ApplicationException;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

public class DeleteFolder {
	private static final Logger log = LoggerFactory.getLogger(DeleteFolder.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(			
			@InputParameter(name="FolderName",constraints= {FOLDER, EXISTS}) String folderName,
			@OutputParameter(name="emptyFolder") ObjectHolder<String> emptyFolder
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			){
				
		try {

			if (folderName != null) {
				File folderToBeDeleted = new File(folderName);
				if (folderToBeDeleted.exists()) {
					deleteFolder(folderToBeDeleted);
					emptyFolder.setValue(folderToBeDeleted.getPath());
				} else
					throw new ApplicationException("Folder does not exist").errorCode("FOLDER_DOES_NOT_EXISTS"); 
					
			} else {
				throw new ApplicationException("Please Specify the folder name").errorCode("FOLDERNAME_IS_NOT_GIVEN"); 
			}

			log.info(folderName + " is deleted");
			return new Status("00","Folder Deleted Successfully" +folderName );
		} catch (Exception e) {
			String className = this.getClass().getSimpleName();

			System.out.println("Display Error code ::" + className);
			return new Status("Error",e.getMessage(),e);

		}
	}


	public static void deleteFolder(File folder) {

		File[] files = folder.listFiles();
		if (files != null) {
			for (File f : files) {
				if (f.isDirectory()) {
					deleteFolder(f);
				} else {
					f.delete();
				}
			}
		}
		folder.delete();
	}

}
