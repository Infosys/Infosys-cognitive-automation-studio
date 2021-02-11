/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/

package com.infosys.impact.botfactory.microbots.db.mongodb;

import static com.infosys.impact.botfactory.microbots.framework.Validation.EXISTS;
import static com.infosys.impact.botfactory.microbots.framework.Validation.DATABASE;

import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.Mongo;
//import com.mongodb.MongoClient;


public class CreateTable  {

	private final Logger log = LoggerFactory.getLogger(CreateTable.class);
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})
	public Status execute(
			@InputParameter(name="Database",constraints= {DATABASE, EXISTS}) String database,
			@InputParameter(name="Table") String table,
			@InputParameter(name="Ip") String ip,
			@InputParameter(name="Port") String port1
//			@OutputParameter(name="Files") ObjectHolder<List<String>> files
			) throws Exception {

		try {
			System.out.println(" CreateTable called inside try................................. ");

			log.info(" print data from execution ................................. " + database + " table " + table);
			int port = Integer.parseInt(port1);
			System.out.println(" CreateTable inside try................................. " + port + " ip " + ip);

			// MongoClient mongoClient = new MongoClient(ip, 27017);
			Mongo mongo = new Mongo(ip, port);
			DB db = mongo.getDB(database);

			DBCollection collection = db.createCollection(table, new BasicDBObject());
			log.info("Table Created  Successfully");
			return new Status("00","Table Created  Successfully" + collection  );

		} catch (Exception e) {
			log.info("Printing Error " + e.toString());
			return new Status("Error",e.getMessage(),e);

		}
	}

}
