#!/home/kk67ctcg/virtualenv/pyapp/3.8/bin/python
from flup.server.fcgi import WSGIServer
from app import app as application
WSGIServer(application).run()