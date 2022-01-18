cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
sleep 3
cd -
cat urlsfortest.txt | xargs -P 4 -n 1 curl 
sleep 2
kill $(ps -aux | grep python3 | awk '{print $2}')
