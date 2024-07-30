# Version - 1.1
# Date - 2019/01/27
# Author - Sam

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from configparser import ConfigParser
from urllib.parse import quote as url_quote
import requests
import json5


class GetVersion:
    @staticmethod
    def show():
        msg = "Guardain-GrafanaWebhook Version:1.0 \n"
        print(msg)
        return


class GetConfig:
    def __init__(self, configfile):
        self.config = ConfigParser()
        self.config.read(configfile)

    # Get Team+ config
    def get_teamplus_api_url(self):
        api_url = self.config.get('TeamPlus', 'api_url')
        return api_url

    def get_teamplus_api_config(self):
        account = self.config.get('TeamPlus', 'account')
        api_key = self.config.get('TeamPlus', 'api_key')
        chat_sn = self.config.get('TeamPlus', 'chat_sn')
        teamplus_config = {'account': account, 'api_key': api_key, 'chat_sn': chat_sn, 'Content_type': '1', 'msg_content': ''}
        return teamplus_config

    # Get this service port
    def get_api_port(self):
        api_port = self.config.get('GrafanaWebhook', 'api_port')
        return api_port

    # Get prefix in config file
    def get_prefix(self):
        prefix = self.config.get('GrafanaWebhook', 'prefix')
        return prefix


# Send message to team+ API
class TeamplusApi:
    def __init__(self, api_url, config):
        self.config = config
        self.api_url = api_url

    def send_message(self, msg):
        self.config['msg_content'] = msg
        return requests.post(self.api_url, self.config).text


# Main class for this API Service
class GrafanaWebhook(Resource):
    def __init__(self):
        # TeamPlus API url & API_KEY
        self.teamplus_url = config.get_teamplus_api_url()
        self.teamplus_config = config.get_teamplus_api_config()
        self.teamplus = TeamplusApi(self.teamplus_url, self.teamplus_config)
        # Get the prefix need to show when alerting in team+
        self.prefix = config.get_prefix()

        # parser api post parameter
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title')
        self.parser.add_argument('ruleId')
        self.parser.add_argument('ruleName')
        self.parser.add_argument('ruleUrl')
        self.parser.add_argument('state')
        self.parser.add_argument('imageUrl')
        self.parser.add_argument('message')
        self.parser.add_argument('evalMatches')

        # Init api parameter
        self.alert = {}

#    def get(self):
#        pass

    def post(self):
        # Get post parameter
        args = self.parser.parse_args()
        self.alert = {'title': args['title'],
                          'ruleId': args['ruleId'],
                          'ruleName': args['ruleName'],
                          'ruleUrl': args['ruleUrl'],
                          'state': args['state'],
                          'imageUrl': args['imageUrl'],
                          'message': args['message'],
                          'evalMatches': args['evalMatches']}
        # Repair string to json format
        broken_json = args['evalMatches'].replace('None','\'\'')
        # Put the metric and value in to self.alert fron broken json
        self.alert['metric'] = json5.loads(broken_json)['metric']
        self.alert['value'] = json5.loads(broken_json)['value']
        # Modify Sting for sending to teamplus
        if self.alert['state'] == 'ok' :
            string = self.alert['title']
        else:
            string = self.alert['title']+'\n'+'---\n'+self.alert['message']+'\n'+self.alert['metric']+'='+str(self.alert['value'])
        # Send message to Teamplus
        self.teamplus.send_message(string)
        return


# Init flask framework
app = Flask(__name__)
api = Api(app)


# API URL = http://{IP}:{Port}/post
api.add_resource(GrafanaWebhook, '/post')

if __name__ == '__main__':
    GetVersion.show()
    config = GetConfig("guardian.conf")
    web_port = config.get_api_port()

    app.run(
        host='0.0.0.0',
        port=web_port,
        debug=True
    )
