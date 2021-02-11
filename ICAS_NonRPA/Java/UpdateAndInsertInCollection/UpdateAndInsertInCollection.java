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
import com.infosys.impact.botfactory.custom.table.UpdateInsertNoSql;
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

public class UpdateAndInsertInCollection {

	private final Logger log = LoggerFactory.getLogger(UpdateAndInsertInCollection.class);
	
	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })

	private MongoClient mongoClient = null;
	private MongoDatabase db = null;
	private MongoCollection<Document> col = null;
	private boolean autoConnect = false;

	public Status execute(@InputParameter(name = MongoConstants.SERVER) String serverObj,
			@InputParameter(name = MongoConstants.INPUT) String input,
			@InputParameter(name = MongoConstants.ISAUTOCONNECT) String autoconn,
			@OutputParameter(name = MongoConstants.UPSERT_OUTPUT) ObjectHolder<String> response) throws Exception {

		autoConnect = Boolean.parseBoolean(autoconn);

		Gson gson = new Gson();
		Server srvDetail = gson.fromJson(serverObj, Server.class);
		UpdateInsertNoSql updateInsertNoSql = gson.fromJson(input, UpdateInsertNoSql.class);

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
					response.setValue(updateInsertCollection(updateInsertNoSql));
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
					response.setValue(updateInsertCollection(updateInsertNoSql));
				}
			}			

			log.info(MongoConstants.UPSERT_OUTPUT + " : " + response);
			return new Status(MongoConstants.SUCCESS_STATUS,MongoConstants.UPSERT_OUTPUT + " : " + response.toString());
			
		} catch (Exception e) {
			response.setValue(e.getMessage().toString());
			log.error(MongoConstants.UPSERT_OUTPUT +" :Exception Occurred : " +response.toString());
			return new Status(MongoConstants.ERROR_STATUS,MongoConstants.UPSERT_OUTPUT +" :Exception Occurred : " + response.toString());
		}
	}

	public String updateInsertCollection(UpdateInsertNoSql updateInsertNoSql) throws Exception {
		log.info("in function");
		
		String tableName=updateInsertNoSql.getTableName();
		
		if(tableName==null){
			return "Please provide table name.";
		}
		
		MongoIterable<String>colList=db.listCollectionNames();
		if(!colList.into(new ArrayList<String>()).contains(tableName)){
			return "Table does not exist";
		}
		
		col = db.getCollection(tableName);

		DbRow row = null;
		DbRow header = updateInsertNoSql.getHeader();
		List<DbRow> rows = updateInsertNoSql.getRows();
		List<String> whereColumns = updateInsertNoSql.getWhereColumns();
		List<Integer> indexForWhereCol = new ArrayList<Integer>();
		
		if(header==null || rows==null||whereColumns==null){
			return "Worng input value. Kindly check the format of input parameter.";
		}
		
		// checking the columns to be matched and polluting it into a list
		for (int i = 0; i < header.getCells().size(); i++) {
			String colName = (String) header.getCells().get(i);
			if (whereColumns.contains(colName)) {
				indexForWhereCol.add(header.getCells().indexOf(colName));
			}
		}

		long oldCount = col.count();
		long updated = 0;

		BasicDBObject searchQuery = new BasicDBObject();
		BasicDBObject query = new BasicDBObject();
		
		String result = "";
		
		for (int i = 0; i < rows.size(); i++) {
			row = rows.get(i);
			for (int j = 0; j < row.getCells().size(); j++) {

				if (indexForWhereCol.contains(j)) {
					// building where query from the where columns list
					searchQuery = searchQuery.append(header.getCells().get(j).toString(), row.getCells().get(j));
				} else {
					// building update query
					query = query.append(header.getCells().get(j).toString(), row.getCells().get(j));
				}
			}
			BasicDBObject updateQuery = new BasicDBObject();

			// joining the queries
			updateQuery.append("$set", query);

			// upsert is always true i.e if row not found it will insert the
			// desired row
			UpdateResult updateResult = col.updateMany(searchQuery, updateQuery, new UpdateOptions().upsert(true));
			updated = updated + updateResult.getModifiedCount();
		}

		long newCount = col.count();
		long inserts = newCount - oldCount;

		result = "{\"Number of Inserts\":" + inserts + ",\"Number of Updates\":" + updated + "}";
		
		log.info("result: " + result);
		return result;
	}
}
