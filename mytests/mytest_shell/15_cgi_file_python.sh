cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
sleep 3
cd -
curl "localhost:8070/cgibin/shellvar.py" | diff - 15_expected.out
kill $(ps -aux | grep python3 | awk '{print $2}')
