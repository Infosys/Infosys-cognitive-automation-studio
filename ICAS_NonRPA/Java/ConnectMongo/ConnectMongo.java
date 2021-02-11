/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.db.mongodb;

import java.io.IOException;

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

public class ConnectMongo {

	private final Logger log = LoggerFactory.getLogger(ConnectMongo.class);
	
	@Errors(exceptions= {
			@Error(errorCode="0102030405", errorMessagePattern ="MISC_IO_EXCEPTION" , exceptionClass=IOException.class)
		})

	public Status execute(
			@InputParameter(name=MongoConstants.SERVER) String serverObj,
			@OutputParameter(name=MongoConstants.CONNECT_OUTPUT) ObjectHolder<String> response
			) throws Exception  {

		MongoClient mongoClient = null;

		try {
			Gson gson = new Gson();
			Server srvDetails = gson.fromJson(serverObj, Server.class);

			MongoClientURI uri = new MongoClientURI(srvDetails.getUrl());
			mongoClient = new MongoClient(uri);
			// setting connection object in env
			System.setProperty(InitialContext.INITIAL_CONTEXT_FACTORY, MongoConstants.CONTEXT_VALUE);
			InitialContext ic = new InitialContext();
			ic.addToEnvironment(MongoConstants.SERVER_KEY + uri.getUsername() + "_" + uri.getHosts().get(0)+"_"+uri.getDatabase(), mongoClient);
			log.info(MongoConstants.CONNECT_OUTPUT + " : Success");
			response.setValue("Success");

		} catch (Exception e) {
			log.error(e.getMessage());
			response.setValue(MongoConstants.CONNECT_OUTPUT+ " : Failure : " + e.toString());
			return new Status(MongoConstants.ERROR_STATUS,response.toString());
		}
		return new Status(MongoConstants.SUCCESS_STATUS,MongoConstants.CONNECT_OUTPUT +" : "+response.toString());
	}
}
