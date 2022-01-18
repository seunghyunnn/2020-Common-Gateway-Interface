cd ../..
python3 webserv.py ./mytests/myconfig/config1.cfg | diff - ./mytests/mytest_shell/3_expected.out 
