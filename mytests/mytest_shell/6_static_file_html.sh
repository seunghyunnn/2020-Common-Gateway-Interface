cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
cd -
sleep 3
curl localhost:8070/html.html | diff -Z - 6_expected.out
kill $(ps -aux | grep python3 | awk '{print $2}')
