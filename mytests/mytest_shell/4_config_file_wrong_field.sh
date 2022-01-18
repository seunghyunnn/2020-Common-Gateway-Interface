cd ../..
python3 webserv.py ./mytests/myconfig/config2.cfg | diff - ./mytests/mytest_shell/4_expected.out 
