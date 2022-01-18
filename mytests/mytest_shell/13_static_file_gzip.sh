cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
sleep 3
cd -
curl -H "Accept-Encoding: gzip" localhost:8070/html.html | gunzip | diff -  ../myfiles/html.html
kill $(ps -aux | grep python3 | awk '{print $2}')
