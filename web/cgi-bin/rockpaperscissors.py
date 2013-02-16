#!C:/Python27/python.exe

import cgi
import cgitb; cgitb.enable()



print "Content-Type: text/html; charset=ISO-8859-1\n\n"

print """
<html>
<body>
<center><h1>Rock Paper Scissors!</h1></center>
<form name="input" action="RPSend.py" method="get">
<form>
<center><input type="radio" name="choice" value="Rock" checked="checked"/> Rock</center><br />
<center><input type="radio" name="choice" value="Paper" />  Paper</center><br />
<center><input type="radio" name="choice" value="Scissors" /> Scissors</center><br />
<center><input type ="submit" value ="Play!!" /></center> 
</form>

"""


 
