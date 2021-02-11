/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
/**
 * 
 */
package com.infosys.impact.botfactory.custom;

import java.io.File;
import java.io.FilenameFilter;
import java.util.Properties;

import javax.swing.filechooser.FileFilter;

/**
 * A <code>FileFilter</code> that can be configured to filter the files in required way. 
 * @author Rajagopal_Neralla
 *
 */
public class ConfigurableFileFilter extends FileFilter implements FilenameFilter{
	/**
	 * The file extensions to be accepted. 
	 */
	String[] fileExetensions;
	/**
	 * The description to displayed in the JFileChooser dialog.  
	 */
	String description;
	/**
	 * Creates new instance of ConfigurableFileFilter.
	 * @param fileExetensions The file extensions to be accepted. 
	 * @param description The description to displayed in the JFileChooser dialog. 
	 */
	public ConfigurableFileFilter(String[] fileExetensions, String description) {
		this.fileExetensions=fileExetensions;
		this.description=description;
	}
	/** 
	 * Overrides  @see javax.swing.filechooser.FileFilter#accept(java.io.File)
	 * Accepts the files with extensions provided in the fileExetensions variable.
	 * @see #fileExetensions
	 * @see javax.swing.filechooser.FileFilter#accept(java.io.File)
	 */
	public boolean accept(File f) {
		if(f.isDirectory()){
			return true;
		}
		if(fileExetensions==null || fileExetensions.length==0){
			return true;
		}
		String fileName=f.getName();
		for(int i=0;i<fileExetensions.length;i++){
			if(fileName.endsWith(fileExetensions[i])){
				return true;	
			}
		}
		return false;
	}
	/**
	 * Overrides  @see javax.swing.filechooser.FileFilter#getDescription()
	 * @see javax.swing.filechooser.FileFilter#getDescription()
	 */
	public String getDescription() {
		return description;
	}
	public boolean accept(File dir, String name) {
		File f=new File(dir,name);
		if(f.isDirectory()){
			return true;
		}
		if(fileExetensions==null || fileExetensions.length==0){
			return true;
		}
		String fileName=f.getName();
		for(int i=0;i<fileExetensions.length;i++){
			if(fileName.endsWith(fileExetensions[i])){
				return true;	
			}
		}
		return false;
	}
	public static FileFilter[] getFileFilter(Properties properties){		
		Object[] objects= properties.keySet().toArray();
		ConfigurableFileFilter[] fileFilters=new ConfigurableFileFilter[objects.length];
		for(int i=0;i<objects.length;i++){
			String[] fileExtensions=((String)objects[i]).split(",");
			String desc=properties.getProperty((String) objects[i]);
			fileFilters[i]=new ConfigurableFileFilter(fileExtensions,desc);
		}
		return fileFilters;
	}
}
