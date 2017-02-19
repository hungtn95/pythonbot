from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
from pylint import epylint as lint
import urllib2
import yaml
import os

config = yaml.load(open('rtmbot.conf', 'r'))

class WritableObject(object):
    "dummy output stream for pylint"
    def __init__(self):
        self.content = []
    def write(self, st):
        "dummy write"
        self.content.append(st)
    def read(self):
        "dummy read"
        return self.content

class SnippetPlugin(Plugin):
    def process_message(self, data):
        if data['file']:
            if data['file']['filetype'] == 'python':
                url = data['file']['url_private']
                req = urllib2.Request(url, None, {"Authorization": "Bearer %s" %config['SLACK_TOKEN']})
                response = urllib2.urlopen(req)
                text = response.read()
                with open('test.py', 'wb') as f:
                    f.write(text)
                (pylint_stdout, pylint_stderr) = lint.py_run('test.py', return_std=True)
                a = pylint_stdout.getvalue()
                if a:
                    self.outputs.append([data['channel'], a])
                else:
                    self.outputs.append([data['channel'], 'Your code is perfect!'])
                # self.outputs.append([data['channel'], pylint_stderr.getvalue()])
                os.remove('test.py')
            else:
                self.outputs.append([data['channel'], "I'm a Python poet but {} is not my expertise!".format(data['file']['filetype'])])