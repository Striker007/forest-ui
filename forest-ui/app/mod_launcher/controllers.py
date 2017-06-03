# -*- coding: utf-8 -*-
"""
    job consumer
    ~~~~~~~~~~~~~~~~
"""
import subprocess
import json
import redis
import logging


logging.basicConfig(level=logging.DEBUG, filename='./controllers.log')
logging.debug(__name__)
logging.debug(__package__)


class JobsQueue(object):

    queue_name = "tasks"
    db_name = "sandboxes"
    instance = None
    code_branch = 'unknown'
    websockets_branch = 'unknown'
    bind_ip = 'unknown'

    def __init__(self, name="default"):
        logging.debug('init Redis conntection')
        try:
            self.instance = redis.StrictRedis(host='localhost', port=6379, db=0)
            self.instance.ping()  # detect connect
            self.name = name
        except:
            logging.warn("Redis connecting trouble")
            raise ValueError

    def pop(self):
        return self.instance.brpop(self.name)[1]

    def push(self, value):
        self.instance.lpush(self.name, value)

    def update_data_set(self, key, value):
        result = self.instance.hget(self.db_name, key)
        result = json.loads(result)
        z = result[key].copy()
        z.update(value)
        result[key] = z
        result = json.dumps(result)
        if not self.instance.hset(self.db_name, key, result):
            return False

        return True


class CliManager(object):

    queue = None

    def __init__(self, queue):
        self.queue = queue

    def run(self):
        data = self.queue.pop()

        if data:
            logging.debug(data)
            data = data.split(":")
            if 2 == len(data):
                sandbox = data[0]
                branch = data[1]

                try:
                    # script = '/home/striker/web/forest/cli_sandbox_start.sh'
                    script = '/data/forest/cli_sandbox_start.sh'
                    # output = subprocess.check_output([script, sandbox, branch], stderr=subprocess.STDOUT)
                    # logging.debug(output)
                except:
                    logging.debug("OMG, something going wrong with sandbox start")

                # TODO insert IPs, State, etc.
                self.queue.update_data_set(sandbox, {"state": "up"})
                return True

            else:
                logging.warn("ERR: consumer - task not parsed")
        else:
            logging.debug("proneslOo")

        return False


queue = JobsQueue("tasks")
cli_manager = CliManager(queue)

while True:
    cli_manager.run()
