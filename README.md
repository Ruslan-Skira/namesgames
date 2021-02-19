**installation on mac m1**
1. pip install
2. error with crypto
 - `brew install pkg-config libffi openssl
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography` 
   - `pip install cryptography`
3. error with psyconpg2. 
   - brew info openssl
   - and echo the variables from there.

Linkedin liblrary 
`https://pypi.org/project/linkedin-sdk/`

**run the tests**

1. `pytest --cov=company --ignore=data --cache-clear  `

New **Access token**
1. Make redirection from port 80 to port 4000 because Linkedin couldn't register redirect uri with port. \
[How to run a server on port 80 as a normal user on Linux?](https://serverfault.com/questions/112795/how-to-run-a-server-on-port-80-as-a-normal-user-on-linux)

      1.1 `sudo iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 80 -j REDIRECT --to-ports 4000`
      
      1.2 Run admin command `manage.py get_access_token`
      
      1.3 Click on redirect url
      
      1.4 After getting token delete redirection `sudo iptables -t nat -D OUTPUT 1`
      
      1.5 Look on the table to check the routing `sudo iptables -t nat --line-numbers -n -L `
      
      1.6 Stop the server on 4000 port. Or kill it   _sudo kill -9 `sudo lsof -t -i:9001`_
      
      
- [linkedin/authorization](https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=foobar&scope=r_liteprofile&client_id=78zqy8vv1aerst&redirect_uri=http%3A%2F%2Fnamesgames.com%2F)   

- [namesgames.com](http://namesgames.com/?code=AQQvYQY0JDA93-rDHmeAIJ5nB1M4wjuX_Cy5i68sEQxwdpMVZIvV08nmgOYSlAKz-THYYt7-Qle9bEkRA6tEV7G_eMhvHQvu39zpToOkZMBQR1-7su7LnHp6nNxBzrTkgkWdfpHgCS9y7_BrnPLcF4CD2ttQVxqgQC4WGBQvni7_FsFsUMI6fsRfZ9rJcA&state=foobar) 

- look on all available urls **./manage.py show_urls**  django_extensions


**How to commit changes in the project**
COMMIT NAME will consist of  "Idtask  titleOfTheTask: what are you doing in the commit.”

"+" new

"-"fix

"~" change something a little bit. \
_example_ git commit -m "NAM-10 change permissions: + implemented new permissions ~ was added changes to bla bla bla - fix tests"
**installation on ubuntu**
1. pipenv shell
2. pipenv sync



CELERY
start: celery -A tasks worker — loglevel=INFO