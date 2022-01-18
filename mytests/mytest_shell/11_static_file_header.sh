cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
sleep 3
cd -
curl -i localhost:8070/css.css | grep "Content-Type" | diff -Z - 11_expected.out
kill $(ps -aux | grep python3 | awk '{print $2}')
