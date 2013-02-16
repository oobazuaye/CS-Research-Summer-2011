#!c:\Python27\python.exe -u

# Import modules for CGI handling 
import cgi, cgitb 
 
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

print "Content-type: text/html"
print
print "<pre>"

#print "The form is"
#print form

L = form.getlist("user")
print "Hello", L[0]

print "</pre>"


