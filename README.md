Linkedin liblrary 
`https://pypi.org/project/linkedin-sdk/`

**run the tests**

1. `pytest --cov=company --ignore=data --cache-clear  `

New **Access token**
1. Make redirection from port 80 to port 4000 because Linkedin couldn't register redirect uri with port.
https://serverfault.com/questions/112795/how-to-run-a-server-on-port-80-as-a-normal-user-on-linux

      1.1 `sudo iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 80 -j REDIRECT --to-ports 4000`
      
      1.2 Run admin command `manage.py get_access_token`
      
      1.3 Click on redirect url
      
      1.4 After getting token delete redirection `sudo iptables -t nat -D OUTPUT 1`
      
      1.5 Look on the table to check the routing `sudo iptables -t nat --line-numbers -n -L `
      
      1.6 Stop the server on 4000 port. Or kill it   _sudo kill -9 `sudo lsof -t -i:9001`_
      