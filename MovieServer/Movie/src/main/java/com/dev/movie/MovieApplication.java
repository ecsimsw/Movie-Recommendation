package com.dev.movie;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@SpringBootApplication
public class MovieApplication extends SpringBootServletInitializer{
	
	@RequestMapping("/movie")
	public String jsp() {
		return "movie";
	}
	
	@RequestMapping("/hello")
	public String function() {
		return "hello";
	}
	
	public static void main(String[] args) {
		SpringApplication.run(MovieApplication.class, args);
	}

}

