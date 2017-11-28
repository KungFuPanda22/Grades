from flask import Flask, render_template,request
#from scrape import find_grades
import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import string
import socket
import httplib
import ssl

def find_grades(username,password):
	
	def connect(self):		#some code to deal with certificate validation
    		sock = socket.create_connection((self.host, self.port),
                                self.timeout, self.source_address)
    		if self._tunnel_host:
    			self.sock = sock
    			self._tunnel()

    		self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)


	httplib.HTTPSConnection.connect = connect
	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent', 'Chrome')]

	# The site we will navigate into, handling it's session
	br.open('https://academics1.iitd.ac.in')

	# View available forms
	for f in br.forms():
	    print f

	# Select the second (index one) form (the first form is a search query box)
	br.select_form(nr=0)

	# User credentials
	br.form['username'] = username
	br.form['password'] = password

	# Login
	br.submit()
	soup = BeautifulSoup(str(br.open(br.geturl()).read()),"lxml")
	link=None
	for i in soup.find_all('a'):
		if 'grade' in str(i.get('href')):
			link=i.get('href')
			break
	if link is None:
		return main()
		#return "Invalid Login!!"
	gradesheet=br.open("https://academics1.iitd.ac.in/Academics/"+link).read()
	return gradesheet
		







app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')



@app.route("/")
def main():	
    return render_template('index.html')

@app.route("/",methods=['POST'])
def main_form():	
	username=request.form['username']
	password=request.form['password']
	return find_grades(username,password)
    	


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run()




