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
import com.infosys.impact.botfactory.custom.table.UpdateNoSqlTable;
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
import com.mongodb.client.model.UpdateOptions;
import com.mongodb.client.result.UpdateResult;

public class UpdateDataIntoCollection {

	private final Logger log = LoggerFactory.getLogger(UpdateDataIntoCollection.class);

	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })

	private MongoClient mongoClient = null;
	private MongoDatabase db = null;
	private MongoCollection<Document> col = null;
	private boolean autoConnect = false;
	private static Map<String, String> operators = MongoConstants.DB_Operators;

	public Status execute(@InputParameter(name = MongoConstants.SERVER) String serverObj,
			@InputParameter(name = MongoConstants.INPUT) String input,
			@InputParameter(name = MongoConstants.ISAUTOCONNECT) String autoconn,
			@OutputParameter(name = MongoConstants.UPDATE_OUTPUT) ObjectHolder<String> response) throws Exception {

		operators = MongoConstants.DB_Operators;

		autoConnect = Boolean.parseBoolean(autoconn);

		Gson gson = new Gson();
		Server srvDetail = gson.fromJson(serverObj, Server.class);
		UpdateNoSqlTable updateNoSqlTable = gson.fromJson(input, UpdateNoSqlTable.class);

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
					response.setValue(updateCollection(updateNoSqlTable));
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
					response.setValue( updateCollection(updateNoSqlTable));
				}
			}

			log.info(MongoConstants.UPDATE_OUTPUT + " : " + response);
			return new Status(MongoConstants.SUCCESS_STATUS,MongoConstants.UPDATE_OUTPUT + " : " +  response.toString());
			
		} catch (Exception e) {
			response.setValue(e.getMessage().toString());
			log.error(response.toString());
			return new Status(MongoConstants.ERROR_STATUS,MongoConstants.UPDATE_OUTPUT + " : Exception Occurred : " +  response.toString());
		}
	}

	public String updateCollection(UpdateNoSqlTable noSqlTable) throws Exception {
		log.info("in function");
		String tableName = noSqlTable.getTableName();

		if (tableName == null) {
			return "Please provide table name.";
		}

		MongoIterable<String> colList = db.listCollectionNames();
		if (!colList.into(new ArrayList<String>()).contains(tableName)) {
			return "Table does not exist";
		}

		col = db.getCollection(tableName);
		long insrt = col.count();

		List<Filter> whereColumns = noSqlTable.getWhereColumns();
		List<Filter> updateColumns = noSqlTable.getUpdateColumns();

		if (whereColumns == null || updateColumns == null) {
			return "Worng input value. Kindly check the format of input parameter.";
		}

		Filter filter = null;
		String result = "";
		
		BasicDBObject searchQuery = new BasicDBObject();

		for (int i = 0; i < whereColumns.size(); i++) {
			// building where query
			filter = whereColumns.get(i);
			searchQuery = searchQuery.append(filter.getColName(),
					new BasicDBObject(operators.get(filter.getOperator()), filter.getValue()));
		}

		BasicDBObject query = new BasicDBObject();

		// building columns to set/update columns query
		for (int i = 0; i < updateColumns.size(); i++) {
			filter = updateColumns.get(i);
			query = query.append(filter.getColName(), filter.getValue());
		}

		BasicDBObject updateQuery = new BasicDBObject();

		// joining the where and update columns query
		updateQuery.append("$set", query);

		result = "{";
		UpdateResult updateResult = null;
		if (noSqlTable.isInsert()) {

			// if isInsert is true i.e if row not available to update it
			// inserts
			// the new row
			updateResult = col.updateMany(searchQuery, updateQuery, new UpdateOptions().upsert(true));
			result = result + "\"Number of Inserts\":" + (col.count() - insrt) + ",";
		} else {

			// do not insert if rows are not in data
			updateResult = col.updateMany(searchQuery, updateQuery);
		}
		long count = updateResult.getModifiedCount();
		result = result + "\"Number of Updates\":" + count + "}";
	
		log.info("result: " + result);
		return result;
	}
}
