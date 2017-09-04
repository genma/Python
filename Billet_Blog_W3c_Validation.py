#!/usr/bin/python
# -*-coding:Utf-8 -*
import os
import configparser
import sys
import time
import json
import commands
import urllib
import feedparser
import requests

html_validator_url = 'https://validator.w3.org/check'
css_validator_url = 'https://jigsaw.w3.org/css-validator/validator'
rss_validator_url = 'https://validator.w3.org/feed/'

# Pour imprimer de messages
def message(msg):
    print >> sys.stderr, msg

def validateHTML(httpURL):
    quoted_filename = urllib.quote(httpURL)
    cmd = ('curl -sG -d uri=%s -d output=json %s'
            % (quoted_filename, html_validator_url))
    # Appel de la validation W3C
    status,output = commands.getstatusoutput(cmd)
    if status != 0:
        raise OSError (status, 'failed: %s' % commande)
    # On recupere une sortie au format json
    try:
        result = json.loads(output)
    except ValueError:
        result = ''
    # Traitement du json pour affichage des lignes
    errors = 0
    warnings = 0
    for msg in result['messages']:
        if 'lastLine' in msg:
            message('%(type)s: line %(lastLine)d: %(message)s' % msg)
        else:
            message('%(type)s: %(message)s' % msg)
        if msg['type'] == 'error':
            errors += 1
        else:
            warnings += 1

def validateCSS(CSSURL):
    quoted_filename = urllib.quote(CSSURL)
    cmd = ('curl -sG -d uri=%s -d output=json %s'
        % (quoted_filename, css_validator_url))
    errorcount = result['cssvalidation']['result']['errorcount']
    warningcount = result['cssvalidation']['result']['warningcount']
    errors += errorcount
    warnings += warningcount
    if errorcount > 0:
        message('errors: %d' % errorcount)
    if warningcount > 0:
        message('warnings: %d' % warningcount)

def validateRSS(RSSURL):
    quoted_filename = urllib.quote(RSSURL)
    cmd = ('curl -sG -d uri=%s -d output=json %s'
        % (quoted_filename, rss_validator_url))
    # TODO A COMPLETER

''' Recuperation du RSS, on parse pour ne récuper
que les 10 derniers articles
'''
config = configparser.ConfigParser()
config.read('Config.ini')
configBlog = config['Blog']
blog_rss = configBlog['filRSS']
feeds = feedparser.parse(blog_rss)
syndication_number = 5
for i in range(0, syndication_number):
    currentURL = feeds.entries[i]['link']
    print ("-------------------------------------------------")
    message('Validation de l\'URL: %s ...' % currentURL)
    print ("-------------------------------------------------")
    message('Liste des erreurs rencontrées')
    validateHTML(currentURL)
    print (" ")
    # Pause
    time.sleep(2)
