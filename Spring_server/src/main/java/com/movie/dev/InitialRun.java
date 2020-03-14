package com.movie.dev;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class InitialRun implements CommandLineRunner{
	
	@Override
    public void run(String... args) throws Exception {
		
    	System.out.println("Spring Application run");
    	
		ConnetArithmeticServer a_server;
    	
        String ip = Application.ip;
        int port = Application.port;
        
    	/// send movie data to a_server
 
        a_server = new ConnetArithmeticServer(ip,port);

    	// will be changed to DB
    	
	    a_server.sendDataFile(Application.data_url);
	    
	    String checkFileSent = a_server.rcvMsg();
	    
	    if(checkFileSent.equals("download_end")){
	    	System.out.println("download_end");
	    }
	    
	    String checkFileLoaded = a_server.rcvMsg();
	    
	    if(checkFileLoaded.equals("fileLoad_end")){
	    	a_server.socketClose();
	    }
	    
	    System.out.println("\n=== request http ===");
    }
}