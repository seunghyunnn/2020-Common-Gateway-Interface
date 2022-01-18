cd ../..
python3 webserv.py nopathcon.cfg | diff - ./mytests/mytest_shell/2_expected.out

