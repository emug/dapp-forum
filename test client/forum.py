#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# Modified by Emanuele Muggiri.

from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from dappforum import ForumManager
import sys
import time
import os
import logging

consMan = ConsensusManager.ConsensusManager ()

# Stop ConsensusManager logger
logger = logging.getLogger('libcontractvm')
logger.disabled = True

consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)

# Shows all posts and comments
while True:
	os.system ('clear')
	print ('Forum:')
	postList = forumMan.listPost ()
	for postid in postList:
		p = forumMan.getPostInfo (postid)	
		print ('post ID:', postid, '\n', ' author:', p['author'], '\n',' title:', p['title'],'\n',' body:', p['body'])
		print('  comments:')
		for commentId in p['comments']:
			c = forumMan.getCommentInfo (commentId)
			print('\t','id:', commentId, '\n\t', '  author:', c['author'], '\n\t', ' comment:', c['comment'])
	time.sleep (10)