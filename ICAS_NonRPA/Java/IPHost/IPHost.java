/*
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
*/
package com.infosys.impact.devbot.microbots;

import java.net.InetAddress;
import java.net.UnknownHostException;

public class IPHost {
	
	public static void main(String[] args) {
	
	InetAddress ip=null;
    String hostname=null;
    try {
        ip = InetAddress.getLocalHost();
        hostname = ip.getHostName();
        System.out.println("Your current IP address : " + ip);
        System.out.println("Your current Hostname : " + hostname);

    } catch (UnknownHostException e) {

        e.printStackTrace();
    }

}
}
