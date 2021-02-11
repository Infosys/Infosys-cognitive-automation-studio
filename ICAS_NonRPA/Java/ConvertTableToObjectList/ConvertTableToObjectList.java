/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.conversions;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.infosys.impact.botfactory.custom.table.Row;
import com.infosys.impact.botfactory.custom.table.Table;
import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "ConvertTableToObjectList", version = "1.0", description = "", botCategory = "Conversion", author = "",
technology = "Java", technologyCode = "01", botCategoryCode = "0A", botId = "01")
public class ConvertTableToObjectList {
	@Errors(exceptions= {
			@Error(errorCode = "010A0111FF", errorMessagePattern = ".*", exceptionClass = IOException.class)
	})
	public Status execute(
			@InputParameter(name="Table" ) Table table,
			@InputParameter(name="className" ) String className,
			@OutputParameter(name="List") ObjectHolder<List<Object>> list
			) throws ExecutionError, IOException  {		
		Row header = table.getHeader();		
		List<Object> output = new ArrayList<>();		
		List<Object> colNames = header.getCells();
		
		Class cls=null;
		try {
			cls = Class.forName(className);
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		for(Row row:table.getRows()) {
			int colCount = header.getCells().size();
			
			Object obj;
			try {
				obj = cls.getDeclaredConstructor().newInstance();
				List<Object> cols= row.getCells();
				for(int i=0;i<colCount;i++) {
					String methodName = "set"+ ((String) colNames.get(i)).substring(0, 1).toUpperCase()
							+ ((String) colNames.get(i)).substring(1);
					Method m = cls.getMethod(methodName, String.class);
					m.invoke(obj, cols.get(i));
				}
				output.add(obj);
			} catch (IllegalAccessException | InstantiationException | NoSuchMethodException | SecurityException | IllegalArgumentException | InvocationTargetException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}			
		}
		list.setValue(output);
		return new Status("00","Created a list of maps");	
		
		
		
	}

}
