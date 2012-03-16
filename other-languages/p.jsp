<%@page import="java.net.*"%>
<%@page import="java.io.*" %>
<%

  String httpTunnel = "http://localhost:8991/";
  String req = request.getQueryString();

  out.print(req);
  URL url = new URL(httpTunnel + "?" + req);
  out.print(url);
  HttpURLConnection con = (HttpURLConnection)url.openConnection();
  con.setDoOutput(true);
  con.setRequestMethod(request.getMethod());

  int clength = request.getContentLength();
  if (clength > 0) {
      con.setDoInput(true);
      InputStream isteam = request.getInputStream();
      OutputStream os = con.getOutputStream();
      
      final int length = 5000;
      byte[] bytes = new byte[length];
      int bytesRead = 0;
      while ((bytesRead = isteam.read(bytes, 0, length)) > 0) {
          os.write(bytes, 0, bytesRead);
      } // while
   } // if
   out.clear();
   out = pageContext.pushBody();
   OutputStream ostream = response.getOutputStream();
   response.setContentType(con.getContentType());
   InputStream in = con.getInputStream();
   final int length = 5000;
   byte[] bytes = new byte[length];
   int bytesRead = 0;
   while ((bytesRead = in.read(bytes, 0, length)) > 0) {
     ostream.write(bytes, 0, bytesRead);
   }

%>
