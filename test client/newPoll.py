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

os.system ('clear')
title = input ('Insert title: ')
n = int(input ('Insert the number of choice: '))

choices = []
for i in range(n):
	choice = input ('Insert choice ' + str(i) + ': ')
	choices.append(choice)
deadline = input ('Insert deadline: ')

try:
	print ('Broadcasted:', forumMan.createPoll (title, choices, deadline))
except:
	print ('Error.')