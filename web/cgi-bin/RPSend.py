#!c:\Python27\python.exe -u

# Import modules for CGI handling 
import cgi, cgitb 
import RPS
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
L = form.getlist("choice")
outcome = RPS.RPS(L[0])
compchoice = outcome[1]
ending = outcome[2]

print "Content-Type: text/html; charset=ISO-8859-1\n\n"
print "<center><h2><font color=blue>You chose", L[0], ".</font></h2></center>"
print "<center><h2><font color=red>The computer chose", compchoice, ".</font></h2></center>"
print "<center><h2><font color=green>So,", ending, "</font></h2></center>"
print """
<Center><FORM><INPUT TYPE="button" VALUE="Play again??" onClick="history.go(-1);
return true;"></FORM></Center>
"""

