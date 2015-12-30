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

def getComment(commentId):
	comment = forumMan.getCommentInfo(commentId)
	if 'error' in comment:
		print (comment['message'])
	else:
		print ('id:',commentId,'\n','author:', comment['author'], '\n','title:', comment['comment'])

os.system ('clear')	
commentId = input ('Insert comment ID: ')
getComment(commentId)
	