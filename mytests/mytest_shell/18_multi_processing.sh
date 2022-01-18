cd ../..
python3 webserv.py ./mytests/myconfig/config.cfg &
sleep 3
cd -
curl "localhost:8070/cgibin/shellvar.py?name=test" >temp
curl "localhost:8070/plaintext.txt">>temp
diff -Z temp 18_expected.out
kill $(ps -aux | grep python3 | awk '{print $2}')
