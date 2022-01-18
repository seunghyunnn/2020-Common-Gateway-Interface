CONTENTS OF THIS FILE
------------------------------------

1. Writing style
2. Assumptions
3. Extension
4. Test cases
 
------------------------------------
1. Writing sytle

The code "webserv.py" follows PEP8 guidelines, except for the following:
	1) -PEP8 : 	Use ''.startswith( ) and ' '. endswith( ) instead of string 
			slicing to check for prefixes or suffixes.
	   -webserv.py :     Used indexing and slicing as it is not checking the guaranteed 			prefixes or suffixes but rather composing other components of 			program with the guaranteed position but variable contents. 
------------------------------------
2. Assumptions

1)This program only handles HTTP 'GET' request. 
2) regarding the content type, 
-This program assumes that if the request contains the requesting file type in 
"Accept" header, it always matches the actual file type requested by the client(extension of the requested file)
-This program assumes that the result of the CGI program will contain the right 
content-type if there exists a content-type header in the result. 
-If there is no extension in a static file's name, or if the result of the CGI program doesn't contain the content-type header, this program sets the content type as "text/html" .
3) This program assumes that there is no colon(:) in the request body. 
4) Even though the function "handle_cgi_file_req" loosely checks, this program assumes that the 
execution of cgi_program will always return the output (This assumption is confirmed by one of the staff members in Ed) and its output is not binary data. 
5) If the fork() fails, this program writes "error" in standard error.
------------------------------------
3. Extension

For extension, this program implemented the gzip If the request send gzip in "Accept-
Encoding" header, then the program will gzip the response body and send it to the client. If the client requested a static file, the server will gzip the contents of the file. If the client requested the CGI file, the server will execute the CGI program and gzip the result of execution as a response body. 
------------------------------------
4. Test cases
1) The structure of test mytests:
-myconfig : a diretory that contains various versions of config files 
	|__config.cfg : contains correct fields, exec for python files
	   config1.cfg : missing one field
	   config2.cfg : contains correct fields, but have an extra field 
                config3.cfg : contains correct fields, exec for bash scripts
	   config4.cfg : contain correct fields, 
		       different ports with rest of the config files
	   *These specific values of  fields should be adjusted.
	   *In this environment, /usr/bin/python3 is used for exec. 
-cgibin : a directory that contains CGI files
	|__shellvar.py  
	    echoing.sh 
-myfiles : a directory that contains static files 
	|__html.html  
	    plaintext.txt
	    css.css
                javascript.js
                xml.xml  (from : onlinerandomtools.com/generate-random-xml)
                different_image.jpg (from https://cdn.pixabay.com/photos/zebra-animal-nature
				-africa-safari-4618513)
                image.jpg (from https://cdn.pixabay.com/photo/2019/11/27/21/13/hair
			-4657887__340.jpg)
-java.js : a file used for testing whether the web-server accesses files that exist in the parent directory.
-mytest_shell : a directory that contains 20 different test cases and its expected output (if there 
is expected output file for a test case, then the name of the expected output file is always
testnum_expected.out)

2)mytest_shell
test script name / existence of expected.out file / config file/used static or cgi file
1_no_config_file.sh / o /- /- 
2_no_path_for_config.sh / o /nopathcon.cfg/-
3_config_file_missing_field.sh / o /config1.cfg /-
4_config_file_wrong_field.sh / o /config2.cfg /-
5_static_file_txt.sh / o /config.cfg /plaintext.txt
6_static_file_html.sh / o /config.cfg /html.html
7_static_file_xml.sh / o /config.cfg /xml.xml
8_static_file_jpeg.sh/ o(image.jpg)/config.cfg/image.jpg
9_static_file_jpeg_diff.sh / o(image.jpg)/config.cfg/different_image.jpg
10_static_file_header.sh / o /config.cfg /javascript.js
11_static_file_header.sh / o /config.cfg /css.css
12_static_file_not_found.sh  / o /config.cfg /java.js
13_static_file_gzip.sh / o (html.html)/config.cfg/ html.html
14_cgi_file_python.sh / o / config.cfg /sellvar.py 
15_cgi_file_python.sh / o / config.cfg /sellvar.py
16_cgi_file_shell.sh / o / config3.cfg / echoing.sh
17_cgi_file_gzip.sh / o / config.cfg /shellvar.py
18_multi_processing.sh/ o / config.cfg/shellvar.py, plaintext.txt
19_concurrent_request.sh / x / config.cfg /urlsfortest.txt (text file containing urls that will be concurrently executed), shellvar.py, html.html, xml.xml
20_port_other_than_8070 / o / config4.cfg/plaintext.txt 
