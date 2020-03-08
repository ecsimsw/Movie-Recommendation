package com.dev.movie;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@RestController
@SpringBootApplication
public class HelloController {
	
	@RequestMapping("/hello")
	//해당 URL로 들어온 애를 아래에서 처리한다라고 하는 안내자이다.
	public String index() {
		return "Hello World! Sobin.";
	}
	
	public static void main(String[] args) {
		SpringApplication.run(HelloController.class, args);
	}
}