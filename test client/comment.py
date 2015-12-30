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
postID =  input ('Insert post ID: ')
comment = input ('Insert comment: ')

try:
	print ('Broadcasted:', forumMan.commentPost (postID, comment))
except:
	print ('Error.')
