# thrift_example

Here is the example to use thrift with python server and php client.

the build.sh is the script to build the client/server code for thrift files. Which you don't need to worry,I pre-generated them for you.

How to run server code
1. create the virutalenv(options)

2. pip install -r requirements.txt

3. go into example folder. 

run ```thrift_example/trunk/example# PYTHONPATH=./py python -m py.server.server```

How to run the client code

1. go int example/php folder. 

run ```php Client.php```

you should see th output
server:
```
Starting the server...
2015-06-29 18:25:29,401 - INFO - Thread-1 - ping()
2015-06-29 18:25:29,402 - INFO - Thread-2 - add(1,1)
calculate(1, Work(comment=None, num1=1, num2=0, op=4))
calculate(1, Work(comment=None, num1=15, num2=10, op=2))
getStruct(1)
```

client:
```
ping()
1+1=2
InvalidOperation: Cannot divide by 0
15-10=5
Log: 5
```
