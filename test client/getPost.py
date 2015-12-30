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

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)

def getPost(postId):
	post = forumMan.getPostInfo(postId)
	if 'error' in post:
		print (post['message'])
	else:
		print ('id:',postId,'\n','author:', post['author'], '\n','title:', post['title'],'\n','body:',post['body'])
		print('\t','comments:')
		comments = post['comments']
		for cid in comments:
			c = forumMan.getCommentInfo(cid)
			print('\t\t','id:',cid, '\n\t\t', 'author:', c['author'], '\n\t\t', 'comment:',c['comment'])


os.system ('clear')	
postId = input ('Insert post ID: ')
getPost(postId)
sys.exit(0)
	