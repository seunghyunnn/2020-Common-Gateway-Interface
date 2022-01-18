cd ../..
python3 webserv.py ./mytests/myconfig/config3.cfg &
sleep 3
cd -
curl "localhost:8070/cgibin/echoing.sh" | diff - 16_expected.out
kill $(ps -aux | grep python3 | awk '{print $2}')
