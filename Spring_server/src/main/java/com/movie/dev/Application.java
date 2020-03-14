package com.movie.dev;

import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.GetMapping;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;


import java.net.*;
import java.io.*;

import java.nio.file.Files;
import java.nio.file.Paths;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


@Controller 
@SpringBootApplication
public class Application {
	public static String data_url = "C:\\Users\\luraw\\OneDrive\\Desktop\\data\\movies_metadata.csv";
	public static String cacheFolder_url = "C:\\Users\\luraw\\git\\movie_recommendation\\Spring_server\\src\\main\\webapp\\WEB-INF\\jsp\\cache\\";
	
	public static String ip = "127.0.0.1";
	public static int port_webPage = 8080;
	public static int port = 8888;
     
    @RequestMapping("/movie") 
    public String jsp(){
       return "movie";
    }
    
    @GetMapping("/result")  
    public String getParameters(@RequestParam String title) {
        System.out.println("Title : "+title);
        
        String result_jsp;
        
        if(isFileExists(cacheFolder_url+title+".jsp")){
        	// There is cache data arleady
        	result_jsp = "cache/"+title;
        }
        
        else {
		  String RcvTitle = title;
		  ConnetArithmeticServer a_server = new ConnetArithmeticServer(ip,port);
		
		  ArrayList<String> lines = a_server.getRecommendation(RcvTitle);
		  result_jsp = makeJspFile(title,lines); 
		  a_server.socketClose();
        }
        
       
        return result_jsp; 
    }    
	
    public static void main(String[] args) {
    	SpringApplication.run(Application.class, args); 
    }
   
	static public String makeJspFile(String title, ArrayList<String> lines) {
		 String url_cache = cacheFolder_url+title+".jsp"; 
		
		 try {
		        String filePath = url_cache;
		        
		        FileWriter fw = new FileWriter(filePath);
		        
		        fw.write("<%@ page language=\"java\" contentType=\"text/html; charset=UTF-8\"\r\n" + 
		        		"\r\n" + 
		        		"    pageEncoding=\"UTF-8\"%>");
		        fw.write("<!DOCTYPE html>\r\n" + 
		        		" <html>\r\n" + 
		        		" \r\n" + 
		        		"\r\n" + 
		        		" <head> \r\n" + 
		        		"   <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"> \r\n" + 
		        		"   <title>Hello Movie Engine</title>\r\n" + 
		        		" </head>\r\n" + 
		        		" <body>");
		        
		        for(String line : lines) {
		        	fw.write(line+"<br>");
		        }
		        
		        fw.write("</body>"+
		        		"</html>");
		       
		       fw.close(); 
		       System.out.println("\n=== jsp complete ===");
		 
		 } catch (Exception e) {
			e.getStackTrace();
		    }
	
	return "cache/"+title;
	}

	static public boolean isFileExists(String file_url) {
		File file = new File(file_url); 
		boolean isExists = file.exists(); 
		
		return isExists;
	}
}



