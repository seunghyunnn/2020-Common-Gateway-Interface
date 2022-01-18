cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
cd -
sleep 3
curl localhost:8070/image.jpg | diff - ../myfiles/different_image.jpg
kill $(ps -aux | grep python3 | awk '{print $2}')
