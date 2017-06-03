# Docker web ui


~ Integrate Docker power in the testing ENV of our Projects ~

(( ... this is beta version of solution - so there are a lack of robustness ...  ))


# documentation isn't completed ...

TOOLS

- docker - containerization platform  https://www.docker.com/
- forest - sandboxes platform (automation tools), abstractio level for docker, config rendering, git interaction, other helpful processes
(maybe we will move to ansible .. )
- forest-ui - pythons web ui, job consumer 
redis - in memory keyval db https://hub.docker.com/_/redis/
(use as queue and like db .. maybe we will move to etcd)
- python env - is a tool to create isolated Python environments.
https://virtualenv.pypa.io/en/stable/
#--------
INSTALLATION:

1) SOFTWARE:
check access to  Docker registry
```sh
cd /data
git clone ...forest-ui  (web ui and consumer)
git clone ...forest
sudo docker run --name some-redis -p 6379:6379 -d redis
(access inside redis: sudo docker exec -it some-redis redis-cli )
sudo pip install virtualenv
cd /data/forest-ui/forest-ui
mkdir env
virtualenv env
 ./env/bin/pip install flask flask-wtf redis
project dependencies php, npm - for composer, npm etc.
```
2) CONFIGURATION
```
/data/forest/configs/main.conf - where are - IPs = sandboxes , ci user, main dir path
```
3) RUN
```
deside that redis is started ( sudo docker ps | grep redis )
cd  /data/forest-ui/forest-ui
./env/bin/python run.py  (web ui) http://server:8041
./env/bin/python app/mod_launcher/controllers.py (consumer, i have to rename this ...) 
 ```
#--------

1) HOW TO USE (WEB UI):
```
a.1) open in browser (any ip of your server and port 8081)
http://10.145.2.141:8081/containers/
U may see web ui with list of active sandboxes and form which uses for start new sandboxes
branch\tag name: any valid branhc\tag
sandbox valid names:
sandbox_10  (it will be 10.145.2.155)
sandbox_20 (10.145.2.156)
sandbox_30 (10.145.2.157)
... has to be configured in /data/forest/configs/main.conf
a.2) press Launch
b) waiting ... its long process to start sandbox > 30sec, U can refresh page from time to time ...
c.1) after above 5-10 min waiting , U can open working (i think so) API  on the sandbox ip http://10.145.2.156/
c.2) if U have got an ssh access to  web147-pangea-testing-all-v  than you can manipulate of settings, contaners, data from server
as an example sandbox_10 dir /data/forest/sandbox-_10/  contain
docker-compose.yml
API code folder with created app/configs/config.yml
PS u can see post install procedures in
/data/forest/mod_code_migrations.sh
```

2) HOW TO USE (TOOLS):
```-- CLEAN
cd /data/forest
./cli_sandbox_destroy.sh sandbox_10
 sudo docker exec -it some-redis redis-cli
FLUSHALL
-- START sandbox
./cli_sandbox_start.sh  sandbox_10  master
```
3) HOW TO USE (WITHOUT EITHER TOOLS AND UI):
```(after sandbox created)
cd /data/forest
cd sandbox_10
manage containers - sudo docker-compose up \ down
edit - api/app/configs/config.yml
```

4) LOGS:
```/data/forest-ui/forest-ui/controllers.log```
