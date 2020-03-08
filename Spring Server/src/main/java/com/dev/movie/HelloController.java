
package com.dev.movie;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.IOException;
import java.net.*;
import java.io.*;

import java.nio.file.Files;
import java.nio.file.Paths;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import java.net.UnknownHostException;

@RestController
@SpringBootApplication
public class HelloController {
    @RequestMapping("/movie")
    //해당 URL로 들어온 애를 아래에서 처리한다라고 하는 안내자이다.
    public String index() {
        return "Hello World! Sobin.";
    }

    public static void main(String[] args) {
        //SpringApplication.run(HelloController.class, args);

        sendDataFile();
    }

    public static void sendDataFile(){
        String url_temp = "C:\\Users\\luraw\\OneDrive\\Desktop\\data\\movies_metadata.csv";
        String ip = "127.0.0.1";
        int port = 7777;
        Socket socket = null;
        ServerSocket server = null;  //서버 생성을 위한 ServerSocket

        try{
            server = new ServerSocket(port);
            System.out.println("Accept : wait for client...");
            socket = server.accept();

            InetAddress inetaddr = socket.getInetAddress();
            System.out.println("Connect : "+ inetaddr.getHostAddress());

            OutputStream out = socket.getOutputStream();
            InputStream in = socket.getInputStream();

            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(out));
            BufferedReader br = new BufferedReader(new InputStreamReader(in));

            String c_msg = br.readLine();

            System.out.println("Received : " + c_msg);

            if(c_msg.equals("client_ready")){
                System.out.println("\n=== client ready ===");
            }

            String s_msg = "server_ready";

            bw.write(s_msg);
            bw.flush();

            System.out.println("Send : " + s_msg);

            c_msg = br.readLine();

            System.out.println("Received : " + c_msg);

            if(c_msg.equals("client_ACK")){
                System.out.println("\n=== download start ===");

                fileSender(url_temp, bw);
                bw.write("\n");
                bw.flush();
                bw.write("!download_end");
                bw.flush();

                System.out.println("\n=== download end ===");
            }

            socket.close();
            server.close();
        } catch(IOException e){
            e.printStackTrace();
        }
    }

    public static void fileSender(String url, BufferedWriter bw ){
        BufferedReader reader = null;

        try{
            reader = new BufferedReader(new FileReader(url));

            //Charset.forName("UTF-8");
            String line = "";

            while((line = reader.readLine())!=null){

                bw.write(line+"\n");
                bw.flush();
            }
        }catch(FileNotFoundException e){
            e.printStackTrace();
        }catch(IOException e) {
            e.printStackTrace();
        }
    }
}
