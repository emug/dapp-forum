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

# Stop ConsensusManager logger
loggerCon = logging.getLogger('libcontractvm')
loggerCon.disabled = True

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)

# Shows all polls
while True:
	os.system ('clear')
	print ('Polls:')
	polls = forumMan.listPolls ()
	for pollid in polls:		
		p = forumMan.getPollInfo(pollid)	
		print ('poll ID:',pollid,'\n',' author:', p['author'], '\n',' title:', p['title'],'\n',' deadline:',p['deadline'])
		if int(time.time()) < p['deadline']:
			print('  state: OPEN')
		else:
			print('  state: CLOSE')
		print('  answers:')
		for answer in p['answers'].keys():
			print('\t' + answer  + ': ' + str(p['answers'][answer]['votes']))
		print('  Votes:')
		for vote in p['votes'].keys():
			print('\t voter:' + vote + ' vote_id:' + p['votes'][vote]['vote_id'] + ' answer:' + p['votes'][vote]['answer'])
	time.sleep (10)