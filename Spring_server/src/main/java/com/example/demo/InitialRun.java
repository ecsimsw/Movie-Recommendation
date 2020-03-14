package com.example.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;


@Component
public class overrideRun implements CommandLineRunner{
	
	@Override
    public void run(String... args) throws Exception {
		 ConnetArithmeticServer a_server;
	    	
	        String ip = Application.ip;
	        int port = Application.port;
	        
	    	/// send movie data to a_server
	 
	        a_server = new ConnetArithmeticServer(ip,port);

	    	String url_temp = "C:\\Users\\luraw\\OneDrive\\Desktop\\data\\test_meta.csv";
	    	
	    	// will be changed to DB
	    	
		    a_server.sendDataFile(url_temp);
		    
		    String checkFileSent = a_server.rcvMsg();
		    
		    if(checkFileSent.equals("download_end")){
		    	a_server.socketClose();
		    	System.out.println("Spring Application run");
		    }
    }
}