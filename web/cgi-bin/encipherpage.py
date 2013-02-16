#!C:/Python27/python.exe

import cgi
import cgitb; cgitb.enable()



print "Content-Type: text/html; charset=ISO-8859-1\n\n"

print """
<html>
<body>
<center><h1>Caesar Encipherrr!</h1></center>
<form name="input" action="encipherresult.py" method="get">
<form>
<center><input type="text" name="code"/> </center>
<center>Enter text to be enciphered here!</center>
<br><br><br>
<center><input type ="submit" value ="Encipher!!" /></center> 
</form>

"""


 
