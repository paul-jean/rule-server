# Cellular automaton server

## Run locally

- clone this repo
```
[rule146@rule146: code]$ git clone git@github.com:paul-jean/rule-server.git
Cloning into 'rule-server'...
```

- cd into the server root `rule`:

```
[rule146@rule146: code]$ cd copy-rule-server/
[rule146@rule146: copy-rule-server]$ lt
total 32
drwxr-xr-x  18 rule146  staff   612B Jan 24 19:44 rule/
-rwxr-xr-x   1 rule146  staff    67B Jan 24 19:44 push.sh*
-rw-r--r--   1 rule146  staff   625B Jan 24 19:44 pg_config.sh
drwxr-xr-x  11 rule146  staff   374B Jan 24 19:44 old/
drwxr-xr-x  16 rule146  staff   544B Jan 24 19:44 images/
-rw-r--r--   1 rule146  staff   762B Jan 24 19:44 Vagrantfile
-rw-r--r--   1 rule146  staff    28B Jan 24 19:44 README.md
[rule146@rule146: copy-rule-server]$ cd rule/
[
```

- install the client libraries
```
[rule146@rule146: rule]$ npm install
...
```

- boot the vagrant VM:
```
[rule146@rule146: rule]$ vagrant up
Bringing machine 'rulehost' up with 'virtualbox' provider...
...
```

- ssh into the VM:
```
[rule146@rule146: rule]$ vagrant ssh
Welcome to Ubuntu 14.04.2 LTS (GNU/Linux 3.13.0-55-generic i686)
...
```

- run the flask project:
```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/rule$ python project.py
 * Running on http://0.0.0.0:5000/
 * Restarting with reloader
```

- navigate to localhost on port 5000 in your browser:
![/images/rule-server-home.png](home page)
