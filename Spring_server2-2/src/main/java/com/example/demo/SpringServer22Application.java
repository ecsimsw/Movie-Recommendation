package com.example.demo;

import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;


@Controller 
@SpringBootApplication
public class SpringServer22Application {
    @RequestMapping("/movie") 
    public String jsp(){
       return "movie";
    }
    
    @GetMapping("/result")  
    public String getParameters(@RequestParam String title){
        System.out.println(title);
    	return "result";
    }    
    public static void main(String[] args) {
        SpringApplication.run(SpringServer22Application.class, args);
    }
    
}