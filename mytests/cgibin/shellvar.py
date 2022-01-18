import os 
if 'QUERY_STRING' in os.environ:
    print(os.environ['QUERY_STRING'])
else :
    print("I didn't get query string")
