/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.db.mongodb;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import javax.naming.InitialContext;

import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;
import com.infosys.impact.botfactory.custom.table.DbRow;
import com.infosys.impact.botfactory.custom.table.DbTable;
import com.infosys.impact.botfactory.domain.Server;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoIterable;

public class InsertDataIntoCollection{

	private final Logger log = LoggerFactory.getLogger(InsertDataIntoCollection.class);
	
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})

	private MongoClient mongoClient = null;
	private MongoCollection<Document> col = null;
	private MongoDatabase db = null;
	private boolean autoConnect = false;

	public Status execute(
			@InputParameter(name=MongoConstants.SERVER) String serverObj,
			@InputParameter(name=MongoConstants.INPUT) String input,
			@InputParameter(name=MongoConstants.ISAUTOCONNECT)String autoconn,
			@OutputParameter(name=MongoConstants.INSERT_OUTPUT) ObjectHolder<String> response
			) throws Exception {

		autoConnect = Boolean.parseBoolean(autoconn);

		Gson gson = new Gson();
		Server srvDetail = gson.fromJson(serverObj, Server.class);
		DbTable table = gson.fromJson(input, DbTable.class);

		MongoClientURI uri = new MongoClientURI(srvDetail.getUrl());
		MongoIterable<String> itr = null;
		try {
			if (autoConnect) {
				mongoClient = new MongoClient(uri);
				itr = mongoClient.listDatabaseNames();
				if (!itr.into(new ArrayList<String>()).contains(uri.getDatabase())) {
					response.setValue("Database does not exists. Please provide the correct name");
				} else {
					db = mongoClient.getDatabase(uri.getDatabase());
					response.setValue(insertDocuments(table));
				}
				mongoClient.close();
			} else {
				// if autoconnect is false--> getting connection object from the
				// env
				// created by ConnectMongo Bot
				System.setProperty(InitialContext.INITIAL_CONTEXT_FACTORY,
						MongoConstants.CONTEXT_VALUE);
				InitialContext ic = new InitialContext();
				Hashtable<?, ?> h = ic.getEnvironment();
				mongoClient = (MongoClient) h
						.get(MongoConstants.SERVER_KEY + uri.getUsername() + "_" + uri.getHosts().get(0)+"_"+uri.getDatabase());
				log.info("MongoClient::" + mongoClient.toString());

				itr = mongoClient.listDatabaseNames();
				if (!itr.into(new ArrayList<String>()).contains(uri.getDatabase())) {
					response.setValue("Database does not exists. Please provide the correct name");
				} else {
					db = mongoClient.getDatabase(uri.getDatabase());
					response.setValue(insertDocuments(table));
				}
			}

			log.info(MongoConstants.INSERT_OUTPUT + " : " + response.toString());
			return new Status(MongoConstants.SUCCESS_STATUS,MongoConstants.INSERT_OUTPUT + " : " + response.toString());
			
		} catch (Exception e) {
			response.setValue( e.getMessage().toString());
			log.error(MongoConstants.INSERT_OUTPUT+" : Exception Occurred : "  +response.toString());
			return new Status(MongoConstants.ERROR_STATUS,MongoConstants.INSERT_OUTPUT+" : Exception Occurred : "  +response.toString());
		}
	}

	public String insertDocuments(DbTable table) throws Exception {
		log.info("Insert: in function");
		String tableName = table.getTableName();

		if (tableName == null) {
			return "Please provide table name.";
		}

		MongoIterable<String> colList = db.listCollectionNames();
		if (!colList.into(new ArrayList<String>()).contains(tableName)) {
			return "Table does not exist";
		}
		col = db.getCollection(tableName);
		long numberOfInsert = 0;
		String response = "";

		ArrayList<Document> list = new ArrayList<>();
		Document document = null;
		DbRow header = table.getHeader();
		List<DbRow> rows = table.getRows();
		
		if(header==null || rows==null){
			return "Worng input value. Kindly check the format of input parameter.";
		}
		
		long oldCount = col.count();

		for (int i = 0; i < rows.size(); i++) {
			DbRow row = rows.get(i);
			document = new Document();
			for (int j = 0; j < header.getCells().size(); j++) {
				document.put(header.getCells().get(j).toString(), row.getCells().get(j));
			}
			log.info("document: " + document.toString());
			list.add(document);
		}

		col.insertMany(list);
		numberOfInsert = col.count() - oldCount;
		log.info("Insert: " + numberOfInsert);
		response = "{\"Number of inserts\":" + numberOfInsert + "}";
	
		return response;
	}
}
