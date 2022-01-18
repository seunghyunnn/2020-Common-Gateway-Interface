cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
sleep 3
cd -
curl -i localhost:8070/java.js | diff -Z - 12_expected.out
kill $(ps -aux | grep python3 | awk '{print $2}')
