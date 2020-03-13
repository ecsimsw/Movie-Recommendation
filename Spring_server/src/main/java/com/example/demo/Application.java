package com.example.demo;

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
	
	public static String ip = "127.0.0.1";
	public static int port = 8888;
     
    @RequestMapping("/movie") 
    public String jsp(){
       return "movie";
    }
    
    @RequestMapping("/hello")
	public String function() {
		return "hello";
	}
    
    @GetMapping("/result")  
    public String getParameters(@RequestParam String title) {
    	// 연산 추천, 추천 영화들 정보를 jsp, 그걸 출력
        System.out.println(title);
        String RcvTitle = title;
        
        ConnetArithmeticServer a_server = new ConnetArithmeticServer(ip,port);
      
	    ArrayList<String> lines = a_server.getRecommendation(RcvTitle);
        makeJspFile(lines); 
        
        return "result"; 
    }    
    
    public static void main(String[] args) {
    	SpringApplication.run(Application.class, args); 
    }
    
	static public void makeJspFile(ArrayList<String> lines) {
		String url_result_jsp = "C:\\Users\\luraw\\git\\movie_recommendation\\Spring_server\\src\\main\\webapp\\WEB-INF\\jsp\\result.jsp";
		  
		 try {
		        String filePath = url_result_jsp; 
		        
		        FileWriter fw = new FileWriter(filePath);
		        
		        for(String line : lines) {
		        	fw.write(line+"\n");
		        }
		       
		       fw.close(); 
		       System.out.println("\n=== jsp complete ===");
		 
		 } catch (Exception e) {
			e.getStackTrace();
		    }
	}
}

class ConnetArithmeticServer{
	String ip;
	int port;
	
	Socket socket = null;
	ServerSocket server = null; 
	OutputStream out = null;
	InputStream in = null;
	
	BufferedWriter bw = null;
	BufferedReader br = null;
	ArrayList<String> lines;
	
	public ConnetArithmeticServer(String ip, int port) {
		this.ip = ip;
		this.port = port;
		
		handshake();
	}
	
	public ArrayList<String> getRecommendation(String rcvdTitle){
		System.out.println("");
		System.out.println("=== send search title ===");
		sendMsg(rcvdTitle);
		
		String msg = rcvMsg();
		
		ArrayList<String> lines = new ArrayList<String>();
		
		if(msg.equals("send_result")){
		System.out.println("\n=== download result ===");
		
		    receiveResult(lines);
		}	
		
		return lines;
	}
	
	public boolean handshake(){
	    try {
	        server = new ServerSocket(port);
	        System.out.println("Accept : wait for client...");
	        socket = server.accept();
	
	        InetAddress inetaddr = socket.getInetAddress();
	        System.out.println("Connect : " + inetaddr.getHostAddress());
	
	        out = socket.getOutputStream();
	        in = socket.getInputStream();
	
	        bw = new BufferedWriter(new OutputStreamWriter(out));
	        br = new BufferedReader(new InputStreamReader(in));
	
	        String c_msg = br.readLine();
	
	        System.out.println("Received : " + c_msg);
	
	        if (c_msg.equals("client_ready")) {
	            System.out.println("\n=== client ready ===");
	        }
	
	        String s_msg = "server_ready";
	
	        bw.write(s_msg);
	        bw.flush();
	
	        System.out.println("Send : " + s_msg);
	
	        c_msg = br.readLine();
	
	        System.out.println("Received : " + c_msg);
	
	        if(c_msg.equals("client_ACK")) {
	            return true;
	        }
	
	    } catch(IOException e){
	        e.printStackTrace();
	    }
	
	    return false;
	}
	
	public boolean sendDataFile(String file_url){
	    try{
	        String c_msg;
	        c_msg = br.readLine();
	
	        System.out.println("Received : " + c_msg);
	
	        if(c_msg.equals("down_start")){
	            System.out.println("\n=== download start ===");
	
	            fileSender(file_url, bw);
	
	            System.out.println("\n=== download end ===");
	        }
	
	
	        return true;
	
	    } catch(IOException e){
	        e.printStackTrace();
	    }
	    return false;
	}
	
	public void fileSender(String url, BufferedWriter bw ){
	    BufferedReader reader = null;
	
	    try{
	        reader = new BufferedReader(new FileReader(url));
	
	        String line = "";
	
	        while((line = reader.readLine())!=null){
	
	            bw.write(line+"\n");
	            bw.flush();
	        }
	
	        bw.write("\n");
	        bw.flush();
	        bw.write("!download_end");
	        bw.flush();
	
	    }catch(FileNotFoundException e){
	        e.printStackTrace();
	    }catch(IOException e) {
	        e.printStackTrace();
	    }
	}
	
	public boolean sendMsg(String msg){
	    try{
	        bw.write(msg);
	        bw.flush();
	
	        System.out.println("Send : " + msg);
	    }catch(IOException e){
	        e.printStackTrace();
	        return false;
	    }
	    return true;
	}
	
	public String rcvMsg(){
	    String c_msg= "";
	    try {
	         c_msg = br.readLine();
	    } catch(IOException e){
	        e.printStackTrace();
	    }
	    return c_msg;
	}
	
	public void receiveResult(ArrayList<String> lines){
	    String msg ="";
	
	    try {
	        while (!((msg = br.readLine()).equals("!download_end"))) {
	            lines.add(msg);
	        }
	    }catch(IOException e){
	        e.printStackTrace();
	    }
	}
	
	public void socketClose(){
	    try{
	        socket.close();
	        server.close();
	
	        System.out.println("\n=== socket close ===");
	    }catch(IOException e) {
	        e.printStackTrace();
	    }
	}

}
    