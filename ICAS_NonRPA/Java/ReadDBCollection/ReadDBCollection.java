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
import java.util.Set;

import javax.naming.InitialContext;
import org.apache.commons.lang3.StringUtils;
import org.bson.Document;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;
import com.infosys.impact.botfactory.custom.table.DbRow;
import com.infosys.impact.botfactory.custom.table.DbTable;
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
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoIterable;

public class ReadDBCollection {

	private final Logger log = LoggerFactory.getLogger(ReadDBCollection.class);

	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })

	private MongoClient mongoClient = null;
	private MongoDatabase db = null;
	private MongoCollection<Document> col = null;
	private MongoClientURI uri = null;
	private Boolean autoConnect = false;
	private Map<String, String> operators = MongoConstants.DB_Operators;

	public Status execute(@InputParameter(name = MongoConstants.SERVER) String serverObj,
			@InputParameter(name = MongoConstants.INPUT) String input,
			@InputParameter(name = MongoConstants.ISAUTOCONNECT) String autoconn,
			@OutputParameter(name = MongoConstants.READ_OBJECT) ObjectHolder<String> response) throws Exception {

		operators = MongoConstants.DB_Operators;

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
					response.setValue(readDbCollection(readNoSqlTable));
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
					response.setValue(readDbCollection(readNoSqlTable));
				}
			}
			
			log.info(MongoConstants.READ_OBJECT + " : " + response.toString());
			return new Status(MongoConstants.SUCCESS_STATUS,MongoConstants.READ_OBJECT + " : " + response.toString());
			
		} catch (Exception e) {
			
			response.setValue( e.getMessage().toString());
			log.error(MongoConstants.READ_OBJECT + " : " +response.toString());
			return new Status(MongoConstants.ERROR_STATUS, MongoConstants.READ_OBJECT + " : Exception Occurred : " +response.toString());
		}	
	}

	public String readDbCollection(ReadNoSqlTable noSqlTable) throws Exception {
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
		long maxRows = col.count();
		if (noSqlTable.getMaxRows() != null) {
			maxRows = noSqlTable.getMaxRows();
		}

		BasicDBObject query = new BasicDBObject();
		List<BasicDBObject> andQuery = new ArrayList<BasicDBObject>();

		List<Filter> filters = noSqlTable.getFilter();
		Filter filter = null;
		FindIterable<Document> fi = null;

		if (filters == null || filters.isEmpty()) {
			fi = col.find();

		} else {
			for (int i = 0; i < filters.size(); i++) {
				filter = filters.get(i);
				andQuery.add(new BasicDBObject(filter.getColName(),
						new BasicDBObject(operators.get(filter.getOperator()), filter.getValue())));
			}
			query.put("$and", andQuery);
			fi = col.find(query);
		}

		MongoCursor<Document> cursor = fi.iterator();

		ArrayList<Object> docs = new ArrayList<>();
		DbRow header = null;
		DbRow row = null;
		List<DbRow> rows = new ArrayList<>();
		List<Object> heads = new ArrayList<>();
		List<Object> cells = new ArrayList<>();
		Gson gson = new Gson();
		int limit = 1;
		// Fill the heads first
		while (cursor.hasNext() && limit <= maxRows) {
			Object doc = cursor.next();
			docs.add(doc);
			JSONObject jsonObject = new JSONObject(gson.toJson(doc));

			Set<String> keys = jsonObject.keySet();
			System.out.println(keys);
			for (Object key : keys) {
				if (!heads.contains(key)) {
					heads.add(key);
				}
			}
			limit++;
		}
		// Now set the rows
		cursor = fi.iterator();
		limit = 1;
		while (cursor.hasNext() && limit <= maxRows) {
			cells = new ArrayList<>();
			row = new DbRow();
			Object doc = cursor.next();
			docs.add(doc);
			JSONObject jsonObject = new JSONObject(gson.toJson(doc));
			for (Object key : heads) {
				if (!jsonObject.has(key.toString())) {
					cells.add(StringUtils.EMPTY);
				} else {
					cells.add(jsonObject.get(key.toString()).toString());
				}
			}
			limit++;
			row.setCells(cells);
			rows.add(row);
		}
		cursor.close();

		header = new DbRow();
		header.setCells(heads);

		DbTable table = new DbTable();
		table.setHeader(header);
		table.setRows(rows);
		table.setTableName(tableName);

		JSONObject jobject = new JSONObject(table);
		log.info(MongoConstants.READ_OBJECT + " : " + jobject.toString());

		return jobject.toString();
	}
}
