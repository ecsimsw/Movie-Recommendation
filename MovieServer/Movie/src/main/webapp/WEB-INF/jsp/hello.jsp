<%@ page language="java" contentType="text/html; charset=UTF-8"

    pageEncoding="UTF-8"%>
<!DOCTYPE html>
 <html>
 <head> 
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> 
	<title>hello</title>

 </head>
 <body>
<%
	request.setCharacterEncoding("UTF-8");
    String str1 = request.getParameter("text1");
    request.setAttribute("sendMsg", str1);
    System.out.println("======"+str1);
    RequestDispatcher dispatcher = request.getRequestDispatcher("result.jsp");
    dispatcher.forward(request, response); 
%>
</body>
</html>