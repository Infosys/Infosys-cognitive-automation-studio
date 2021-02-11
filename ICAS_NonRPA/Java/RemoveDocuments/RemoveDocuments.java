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
import java.util.Map;

import javax.naming.InitialContext;

import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;
import com.infosys.impact.botfactory.custom.table.Filter;
import com.infosys.impact.botfactory.custom.table.ReadNoSqlTable;
import com.infosys.impact.botfactory.domain.Server;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoIterable;
import com.mongodb.client.result.DeleteResult;

public class RemoveDocuments {

	private final Logger log = LoggerFactory.getLogger(RemoveDocuments.class);
	
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})

	private MongoClient mongoClient = null;
	private Boolean deleteOne = null;
	private MongoDatabase db = null;
	private MongoCollection<Document> col = null;
	private MongoClientURI uri = null;
	private Boolean autoConnect = false;
	private Map<String, String> operators = MongoConstants.DB_Operators;

	public Status execute(
			@InputParameter(name=MongoConstants.SERVER) String serverObj,
			@InputParameter(name=MongoConstants.INPUT) String input,
			@InputParameter(name=MongoConstants.ISDELETEONE)String delete,
			@InputParameter(name=MongoConstants.ISAUTOCONNECT)String autoconn,
			@OutputParameter(name=MongoConstants.DELETE_OUTPUT) ObjectHolder<String> response
			) throws Exception  {
		
		operators = MongoConstants.DB_Operators;		
		deleteOne = Boolean.parseBoolean(delete);
		autoConnect = Boolean.parseBoolean(autoconn);
		Gson gson = new Gson();
		Server srvDetail = gson.fromJson(serverObj, Server.class);
		ReadNoSqlTable readNoSqlTable = gson.fromJson(input, ReadNoSqlTable.class);

		uri = new MongoClientURI(srvDetail.getUrl());
		MongoIterable<String> itr = null;

		try {
			if (autoConnect) {
				mongoClient = new MongoClient(uri);
				itr = mongoClient.listDatabaseNames();
				if (!itr.into(new ArrayList<String>()).contains(uri.getDatabase())) {
					response.setValue("Database does not exists. Please provide the correct name");
				} else {
					db = mongoClient.getDatabase(uri.getDatabase());
					response.setValue(removeDocument(readNoSqlTable));
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
					response.setValue(removeDocument(readNoSqlTable));
				}
			}
			
			log.info(MongoConstants.DELETE_OUTPUT + " : " + response.toString());
			return new Status(MongoConstants.SUCCESS_STATUS, MongoConstants.DELETE_OUTPUT + " : "+response.toString());

		} catch (Exception e) {
			response.setValue( e.getMessage().toString());
			log.error(response.toString());
			return new Status(MongoConstants.ERROR_STATUS,MongoConstants.DELETE_OUTPUT+" : Exception Occurred : " + response.toString());
		}		
	}

	public String removeDocument(ReadNoSqlTable readNoSqlTable) throws Exception{
		String response = "";

		String tableName = readNoSqlTable.getTableName();

		if (tableName == null) {
			return "Please provide table name.";
		}

		MongoIterable<String> colList = db.listCollectionNames();
		if (!colList.into(new ArrayList<String>()).contains(tableName)) {
			return "Table does not exist";
		}

		col = db.getCollection(tableName);

		BasicDBObject query = new BasicDBObject();
		List<BasicDBObject> andQuery = new ArrayList<BasicDBObject>();

		List<Filter> filters = readNoSqlTable.getFilter();
		Filter filter = null;
		DeleteResult dr = null;
		
		if (filters == null || filters.isEmpty()) {
			return "Add filter in input parameter.";

		} else {
			for (int i = 0; i < filters.size(); i++) {
				filter = filters.get(i);
				andQuery.add(new BasicDBObject(filter.getColName(),
						new BasicDBObject(operators.get(filter.getOperator()), filter.getValue())));
			}
			query.put("$and", andQuery);
			if (deleteOne) {
				dr = col.deleteOne(query);
			} else {
				dr = col.deleteMany(query);
			}
			response = "{\"Number of Deleted rows\" : \"" + dr.getDeletedCount() + "\"}";
		}
		
		return response;
	}
}
