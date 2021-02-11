/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.folder;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.infosys.impact.botfactory.custom.Utility;
import com.infosys.impact.botfactory.domain.Template;
import com.infosys.impact.botfactory.repository.ConfigurationEntryRepository;
import com.infosys.impact.botfactory.repository.TemplateRepository;

/*import com.infosys.impact.devbot.custom.AppGenerationJob;
import com.infosys.impact.devbot.custom.Utility;
import com.infosys.impact.devbot.domain.Template;
import com.infosys.impact.devbot.repository.ConfigurationEntryRepository;
import com.infosys.impact.devbot.repository.TemplateRepository;*/
@Component
public class CopyNodeModulesJob {
	@Autowired
	private ConfigurationEntryRepository configRepository;
	
	@Autowired
	private TemplateRepository templateRepository;
	
	private static final Logger log = LoggerFactory.getLogger(CopyNodeModulesJob.class);
	
	@Scheduled(fixedRate = 60000)
	public void copyNodeModules() {
		File tempLocation = Utility.getActualLocation(configRepository, "TEMP", "");
		log.info("******** In Appgenration tmp location is ::" + tempLocation);
		String[] templateIds = getTemplateIds(tempLocation);
		for(String templateId:templateIds) {
			File template = new File(tempLocation,"node_modules_"+templateId);
			if(template.exists()) {
				replicateTemplate(tempLocation,templateId);
			}else {
				log.info("No template available for " + templateId +"--- "+template.getPath());		
			}
		}		
	}
	private String[] getTemplateIds(File location) {
		Template withoutTemplateObj = new Template();
		withoutTemplateObj.setId(-1l);
		withoutTemplateObj.setTemplateName("without_template");//setName 
		List<Template> templates= templateRepository.findAll();
		templates.add(withoutTemplateObj);
		String[] templateIds=new String[templates.size()];
		for(int i=0;i<templateIds.length;i++) {
			templateIds[i]=templates.get(i).getTemplateName();//FIXME
		}
		return templateIds;
	}
	public void replicateTemplate(File tempLocation,String templateId) {
		int nodeModuleCount[] = findMissingFolders(tempLocation,templateId);
		System.out.println("********** Get Count of Node Modules " + nodeModuleCount.length);		
		File srcFolder = tempLocation;
		String folderName = "node_modules_"+templateId;
		for (int i : nodeModuleCount) {
			String destFolderName = i + "_" + folderName;
			File destFolders = new File(tempLocation + "\\" + destFolderName);
			File sourceFolder = new File(srcFolder + "\\" + folderName);
			try {
				copyFolder(sourceFolder, destFolders);
			} catch (IOException e) {
				e.printStackTrace();
			}
			File reNameFolder = new File(tempLocation + "\\" + folderName + "_" + i);
			destFolders.renameTo(reNameFolder);

			System.out.println("********* Node Modules Copied Successfully...******** ");
		}

	}
	private int[] findMissingFolders(File location,String templateId) {
		ArrayList<Integer> l = new ArrayList<Integer>();
		for (int i = 1; i <= 5; i++) {
			if (new File(location, "node_modules_"+templateId+"_"+ i).exists() || new File(location, i + "_node_modules_"+templateId).exists()) {
				if(new File(location, i + "_node_modules_"+templateId+"\\inprogress.txt").exists()) {
					l.add(i);	
				}
			} else {
				l.add(i);
			}
		}
		int[] il = new int[l.size()];
		for (int i = 0; i < il.length; i++) {
			il[i] = l.get(i);
		}
		return il;
	}	
	public static void copyFolder(File src, File dest) throws IOException {
		if(dest.isFile() && dest.exists() && dest.lastModified()==src.lastModified()) {
			log.debug("Dstination "+dest.getAbsolutePath()+" already exists and has same timestamp. Ignoring");
			return;
		}
		if (src.isDirectory()) {
			if (!dest.exists()) {
				dest.mkdir();				
			}
			File inp= new File(dest,"inprogress.txt");
			inp.createNewFile();
			String files[] = src.list();
			for (String file : files) {
				File srcFile = new File(src, file);
				File destFile = new File(dest, file);
				copyFolder(srcFile, destFile);
			}
			inp.delete();			
		} else {
			// if file, then copy it
			// Use bytes stream to support all file types
			InputStream in = new FileInputStream(src);
			OutputStream out = new FileOutputStream(dest);
			byte[] buffer = new byte[1024];
			int length;
			// copy the file content in bytes
			while ((length = in.read(buffer)) > 0) {
				out.write(buffer, 0, length);
			}
			in.close();
			out.close();
		}
		dest.setLastModified(src.lastModified());
	}
	public static void main(String[] args) {
		CopyNodeModulesJob job=new CopyNodeModulesJob();
		File tempLocation = new File("D:\\Code\\Impact\\Temp");
		log.info("******** In Appgenration tmp location is ::" + tempLocation);
		String[] templateIds = new String[] {"AppTemplate1","AppTemplate2"};
		for(String templateId:templateIds) {
			File template = new File(tempLocation,"node_modules_"+templateId);
			if(template.exists()) {
				job.replicateTemplate(tempLocation,templateId);
			}else {
				log.info("No template available for " + templateId);		
			}
		}	
	}
}
