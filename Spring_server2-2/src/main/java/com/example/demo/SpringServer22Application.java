package com.example.demo;

import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.GetMapping;

import java.net.*;
import java.io.*;

import java.nio.file.Files;
import java.nio.file.Paths;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


@Controller 
@SpringBootApplication
public class SpringServer22Application {
    static String url_temp = "C:\\Users\\luraw\\OneDrive\\Desktop\\data\\movies_metadata.csv";
    static String url_result_jsp = "C:\\Users\\luraw\\git\\movie_recommendation\\Spring_server2-2\\src\\main\\webapp\\WEB-INF\\jsp\\result.jsp";
    // 이건 db로 바꿀거고
    
    static String ip = "127.0.0.1";
    static int port = 8080;
    static Socket socket = null;
    static ServerSocket server = null; 
    static OutputStream out = null;
    static InputStream in = null;

    static BufferedWriter bw = null;
    static BufferedReader br = null;
    static ArrayList<String> lines;
    
    @RequestMapping("/movie") 
    public String jsp(){
       return "movie";
    }
    
    @GetMapping("/result")  
    public String getParameters(@RequestParam String title){
        System.out.println(title);
        String RcvTitle = title;
        
        get_rcm_arithmeticServer(RcvTitle);
        
    	return "result";
    }    
    
    public static void main(String[] args) {
    
    SpringApplication.run(SpringServer22Application.class, args);
    
    }
    
    // 클래스로 따로 빼는게 나은거 같음. 변수랑
    public static void get_rcm_arithmeticServer(String rcvdTitle) {
    	handshake();
        sendDataFile();

        // get search_title

        System.out.println("");
        System.out.println("=== send search title ===");
        sendMsg(rcvdTitle);

        String msg = rcvMsg();

        ArrayList<String> lines = new ArrayList<String>();

        if(msg.equals("send_result")){
            System.out.println("=== download result ===");

            receiveResult(lines);
        }

        makeFile(lines);

        socketClose();
    }
    
	public static boolean handshake(){
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
	
	public static boolean sendDataFile(){
	    try{
	        String c_msg;
	        c_msg = br.readLine();
	
	        System.out.println("Received : " + c_msg);
	
	        if(c_msg.equals("down_start")){
	            System.out.println("\n=== download start ===");
	
	            fileSender(url_temp, bw);
	
	            System.out.println("\n=== download end ===");
	        }
	
	
	        return true;
	
	    } catch(IOException e){
	        e.printStackTrace();
	    }
	    return false;
	}
	
	public static void receiveResult(ArrayList<String> lines){
	    String msg ="";
	
	    try {
	        while (!((msg = br.readLine()).equals("!download_end"))) {
	            lines.add(msg);
	        }
	    }catch(IOException e){
	        e.printStackTrace();
	    }
	}
	
	public static void fileSender(String url, BufferedWriter bw ){
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
	
	public static boolean sendMsg(String msg){
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
	
	public static String rcvMsg(){
	    String c_msg= "";
	    try {
	         c_msg = br.readLine();
	    } catch(IOException e){
	        e.printStackTrace();
	    }
	    return c_msg;
	}
	
	public static void socketClose(){
	    try{
	        socket.close();
	        server.close();
	
	        System.out.println("=== close ===");
	    }catch(IOException e) {
	        e.printStackTrace();
	    }
	}
	
	public static void makeFile(ArrayList<String> lines) {
		 try {
		       // 바이트 단위로 파일읽기
		        String filePath = url_result_jsp; 
		        
		        FileWriter fw = new FileWriter(filePath);
		        
		        for(String line : lines) {
		        	fw.write(line+"\n");
		        }
		       
		       fw.close(); //스트림 닫기
		       System.out.println("\n=== jsp complete ===");
		 
		 } catch (Exception e) {
			e.getStackTrace();
		    }
	}
}
    