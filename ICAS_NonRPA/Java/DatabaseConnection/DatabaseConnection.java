/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DatabaseConnection implements JavaDelegate {
	private static final Logger log = LoggerFactory.getLogger(DatabaseConnection.class);

	public void execute(DelegateExecution execution) throws Exception {
		String connection_type = (String) execution.getVariable("connection_type");
		String database_name = (String) execution.getVariable("database_name");
		String server_name = (String) execution.getVariable("server_name");
		String sql_port = (String) execution.getVariable("sql_port");
		String user_name = (String) execution.getVariable("user_name");
		String pass_word = (String) execution.getVariable("pass_word");
		String db_url = null;
		String response = null;

		log.info("Database Connection called............................................");
		log.info("database type===" + connection_type);
		if (user_name == null || pass_word == null) {
			log.info("Either username or passord is null.");
		}
		Connection connection = null;

		if (connection_type.equalsIgnoreCase("mysql")) {
			db_url = "jdbc:mysql://" + server_name + ":" + sql_port + "/" + database_name;
		}
		if (connection_type.equalsIgnoreCase("sqlserver")) {
			db_url = "jdbc:sqlserver://localhost\\sqlexpress";
		}
		if (connection_type.equalsIgnoreCase("oracle")) {
			db_url = "jdbc:oracle:thin:@localhost:1521:xe";
		}

		if (connection_type.equalsIgnoreCase("postgres")) {

			db_url = "jdbc:postgresql://" + server_name + ":" + sql_port + "/" + database_name;
		}

		try {

			connection = DriverManager.getConnection(db_url, user_name, pass_word);
			if (!connection.isClosed()) {
				response = "Yes";
				log.info("Database connected successfully");
			} else {
				response = "No";
				log.info("Database not connected ");
			}

		} catch (SQLException e) {
			System.out.println("Database error:");
			e.printStackTrace();
		}

		execution.setVariable("response", response);

		execution.setVariable("db_url", db_url);
		execution.setVariable("user_name", user_name);
		execution.setVariable("pass_word", pass_word);

	}

}