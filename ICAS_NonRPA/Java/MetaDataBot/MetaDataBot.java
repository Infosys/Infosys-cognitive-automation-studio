/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.java;

/*
 * Fetch tables from mysql database
 */
import java.sql.Connection;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Status;

//import com.infosys.impact.botfactory.config.MySQLDatabaseConfiguration;

public class MetaDataBot {
	private final Logger log = LoggerFactory.getLogger(MetaDataBot.class);

	public Status execute(

	) throws Exception {
		log.info(" Working With Metadata");
		StringBuffer tableName = null;
		Connection con = null;
		try {
			return new Status("00","successfull");

		} catch (Exception e) {
			log.error(e.getMessage());
			return new Status("Error",e.getMessage(),e);
		}

	}

}
