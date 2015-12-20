"""
Rule server: provides an API to run 1D cellular automaton rules
Author: Paul-Jean Letourneau
Date: Dec 2015
"""

"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem, User
from bleach import clean
from random import randrange
from re import sub
from flask import session as login_session
import random, string
from db_link import getDBLink
from functools import wraps
from urlparse import urlparse
from dict2xml import dict2xml as xmlify
from flask import Response

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# init Flask
app = Flask(__name__)
"""

"""
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Random Noms"

# init SQLAlchemy
Base = declarative_base()
dblink = getDBLink()
engine = create_engine(dblink)
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()
"""

def rule_table(rule_num):
    # TODO: restrict to range 0 to 255
    # convert the rule_num to a binary 8-bit string
    bin_string = '{0:08b}'.format(rule_num)
    # enumerate 3-cell neighborhoods
    neighborhoods = ['{:03b}'.format(x) for x in range(7, -1, -1)]
    rule_map = dict(zip(neighborhoods, bin_string))
    return rule_map

def step(rule_map, row):
    # extract neighborhoods
    # left periodic boundary:
    first_nb = '{l}{m}{r}'.format(l=row[-1], m=row[0], r=row[1])
    # right periodic boundary:
    last_nb = '{l}{m}{r}'.format(l=row[-2], m=row[-1], r=row[0])
    new_row = ['{nb[0]}{nb[1]}{nb[2]}'.format(nb=row[i-1:i+2]) for i in range(1, len(row)-1)]
    new_row = [first_nb] + new_row + [last_nb]
    new_row = [rule_map[nb] for nb in new_row]
    return new_row

def run(rule_num, width=100, steps=100):
    """
    Runs rule rule_num for the given number of steps.

    Args:
        rule_num

    Returns:
        An array containing the cell values from the evolution.
    """
    rule_map = rule_table(rule_num)


"""
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
"""
