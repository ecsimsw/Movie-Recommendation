<%@ page language="java" contentType="text/html; charset=UTF-8"

    pageEncoding="UTF-8"%>
<HTML>
    <HEAD><TITLE>제발..</TITLE></HEAD>
    <BODY>
    <% 
    response.setContentType("text/html; charset=UTF-8");
    out.println("입력된 제목"+request.getAttribute("sendMsg"));%>
        
    </BODY>
</HTML>