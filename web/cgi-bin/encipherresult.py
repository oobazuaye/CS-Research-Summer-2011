#!c:\Python27\python.exe -u

# Import modules for CGI handling 
import cgi, cgitb 
import encipher
# Create instance of FieldStorage 

form = cgi.FieldStorage()
L = form.getlist("code")
text = encipher.encipher(L[0], 1)


print "Content-Type: text/html; charset=ISO-8859-1\n\n"
print "<center><h2><font color=blue>The enciphered text now reads: </font></h2></center>"

print "<b><center><font size=20>", text, "</font></center></b><br><br><br>"
print """
<Center><FORM><INPUT TYPE="button" VALUE="Encipher again??" onClick="history.go(-1);
return true;"></FORM></Center>
"""
