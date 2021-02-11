/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.db.mongodb;

import java.io.IOException;
import java.util.Hashtable;

import javax.naming.InitialContext;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;
import com.infosys.impact.botfactory.domain.Server;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.ObjectHolder;
import com.infosys.impact.botfactory.microbots.framework.OutputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;

public class ReleaseConnection {

	private final Logger log = LoggerFactory.getLogger(ReleaseConnection.class);

	@Errors(exceptions = {
			@Error(errorCode = "0102030405", errorMessagePattern = "MISC_IO_EXCEPTION", exceptionClass = IOException.class) })

	public Status execute(@InputParameter(name = MongoConstants.SERVER) String serverObj,
			@OutputParameter(name = MongoConstants.RELEASE_OUTPUT) ObjectHolder<String> result) throws Exception {

		Gson gson = new Gson();
		Server srvDetail = gson.fromJson(serverObj, Server.class);

		try {
			
			MongoClientURI uri = new MongoClientURI(srvDetail.getUrl());
			MongoClient mongoClient = null;
			
			// getting connection object from the env created by ConnectMongo
			// Bot
			System.setProperty(InitialContext.INITIAL_CONTEXT_FACTORY, MongoConstants.CONTEXT_VALUE);
			InitialContext ic = new InitialContext();
			Hashtable<?, ?> h = ic.getEnvironment();
			mongoClient = (MongoClient) h
					.get(MongoConstants.SERVER_KEY + uri.getUsername() + "_" + uri.getHosts().get(0)+"_"+uri.getDatabase());
			mongoClient.close();
			
			result.setValue(MongoConstants.RELEASE_OUTPUT + " : " + "Connection closed/Released");
			log.info(MongoConstants.RELEASE_OUTPUT + " : " + result);
			return new Status(MongoConstants.SUCCESS_STATUS, MongoConstants.RELEASE_OUTPUT + " : " + result.toString());
			
		} catch (Exception e) {
			
			result.setValue(e.getMessage().toString());
			log.error(result.toString());
			return new Status(MongoConstants.ERROR_STATUS, MongoConstants.RELEASE_OUTPUT + " : Exception : " + result.toString());
		}
	}
}
