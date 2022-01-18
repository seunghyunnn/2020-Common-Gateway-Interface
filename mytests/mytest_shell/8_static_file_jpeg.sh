cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
cd -
sleep 1
curl localhost:8070/image.jpg | diff - ../myfiles/image.jpg
kill $(ps -aux | grep python3 | awk '{print $2}')
