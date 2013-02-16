#!C:/Python27/python.exe

import cgi
import cgitb; cgitb.enable()

# this variable, form, holds the data passed into this Python script
form = cgi.FieldStorage()

# this gets a list of all inputs named "name"
L = form.getlist( "name" ) 

# next, we check if any inputs have come in
if len(L) == 0:
    name = "NoName"
else:
    name = L[0]  # take the first input


print "Content-Type: text/html; charset=ISO-8859-1\n\n"
print 

print """
<html>
<body>
<h1>Hello from Python!</h1>
"""

print "<h2><font color=blue>Welcome", name, "</font></h2>"

print """
</body>
</html>
"""
