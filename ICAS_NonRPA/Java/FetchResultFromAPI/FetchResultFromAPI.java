/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.botfactory.microbots.file;

import static com.infosys.impact.botfactory.microbots.framework.Validation.VALID_URL;
import static com.infosys.impact.botfactory.microbots.framework.Validation.NOT_NULL;

import java.io.IOException;

import org.apache.http.HttpException;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CookieStore;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.protocol.HttpClientContext;
import org.apache.http.impl.client.BasicCookieStore;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.infosys.impact.botfactory.microbots.framework.Bot;
import com.infosys.impact.botfactory.microbots.framework.Error;
import com.infosys.impact.botfactory.microbots.framework.Errors;
import com.infosys.impact.botfactory.microbots.framework.ExecutionError;
import com.infosys.impact.botfactory.microbots.framework.InputParameter;
import com.infosys.impact.botfactory.microbots.framework.Status;

@Bot(name = "FetchResultFromAPI", version = "1.0", description = "Fetch the Rest API response", botCategory = "String", author = "",
	technology = "Java", technologyCode = "01", botCategoryCode = "11", botId = "01")


public class FetchResultFromAPI {	
	private static final Logger log = LoggerFactory.getLogger(FetchResultFromAPI.class);
	@Errors(exceptions= {
			@Error(errorCode="01110111FF", errorMessagePattern = ".*", exceptionClass = Exception.class)
		})
public Status execute(
			@InputParameter(name="url", constraints = { VALID_URL }) String url,
			@InputParameter(name="username") String username,
			@InputParameter(name="password") String password
			//@OutputParameter(name="strresp") ObjectHolder<String> strresp
	) throws ExecutionError,IOException {		

		log.info(url);
		log.info(username);
		log.info(password);
			String strresp;
			strresp = ""; 
			
//		String botErrorCode;
//		String errorCategoryCode;
//		String errorCodeA = "1";
//		String errorCodeB;
//		String errorDescrption;
		
	
		try{

			strresp=this.getRequest(url,username,password);
			log.info("Result===="+strresp);
			return new Status("00",	"Fetched data Successfully");
		}catch (Exception e) {
			String className = this.getClass().getSimpleName();
			e.printStackTrace();
			return new Status("Error",e.getMessage(),e);
		}
	}	
		
public String getRequest(String url,String username,String password) throws HttpException, IOException {
		String strresp;
		strresp = "";
     HttpHost proxy = new HttpHost("10.68.248.102",80,"http");
 	//DefaultProxyRoutePlanner routePlanner = new DefaultProxyRoutePlanner(proxy);
		CookieStore cookieStore = new BasicCookieStore();
		HttpContext httpContext = new BasicHttpContext();
		httpContext.setAttribute(HttpClientContext.COOKIE_STORE, cookieStore);
		CredentialsProvider credsProvider = new BasicCredentialsProvider();
		credsProvider.setCredentials(
									new AuthScope(new HttpHost(url)),
									new UsernamePasswordCredentials(username, password));
		CloseableHttpClient httpclient = HttpClients.custom()
											.setDefaultCredentialsProvider(credsProvider)//.setRoutePlanner(routePlanner)
											.build();
		try {
			HttpGet httpget = new HttpGet(url);
			//HttpGet httpget = new HttpGet("https://www.google.com/");
			httpget.setHeader("Accept", "application/json");
			System.out.println("Executing request " + httpget.getRequestLine());
			CloseableHttpResponse response = httpclient.execute(httpget,httpContext);
			try {
				System.out.println("----------------------------------------");
				System.out.println(response.getStatusLine());
				String responseBody = EntityUtils.toString(response.getEntity());
				System.out.println(responseBody);
				strresp = responseBody ;
			} finally {
				response.close();
			}
		}
		finally {
			httpclient.close();
		}

        return strresp;

	}

}
	
