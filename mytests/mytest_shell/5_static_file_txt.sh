cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
cd -
sleep 3
curl localhost:8070/plaintext.txt | diff -Z - 5_expected.out 
kill $(ps -aux | grep python3 | awk '{print $2}')

