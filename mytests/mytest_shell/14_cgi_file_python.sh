cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
sleep 3
cd -
curl "localhost:8070/cgibin/shellvar.py?name=test&age=100" | diff - 14_expected.out
kill $(ps -aux | grep python3 | awk '{print $2}')
