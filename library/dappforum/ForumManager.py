# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# Modified by Emanuele Muggiri.

import time
import logging
from contractvmd import config
from libcontractvm import Wallet, ConsensusManager, DappManager

logger = logging.getLogger(config.APP_NAME)

class ForumManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet = None):
		super (ForumManager, self).__init__(consensusManager, wallet)
	
	# Basic features (forum)
	def createPost (self, title, body):
		cid = self.produceTransaction ('dappforum.createPost', [title, body])
		return cid

	def listPost (self):
		return self.consensusManager.jsonConsensusCall('dappforum.listPost', [])['result']

	def listComment (self):
		return self.consensusManager.jsonConsensusCall('dappforum.listComment', [])['result']

	def getPostInfo (self, postId):
		return self.consensusManager.jsonConsensusCall('dappforum.getPostInfo', [postId])['result']				

	def getCommentInfo (self, commentId):
		return self.consensusManager.jsonConsensusCall('dappforum.getCommentInfo', [commentId])['result']				

	def commentPost (self, postId, comment):
		cid = self.produceTransaction ('dappforum.commentPost', [postId, comment])
		return cid

	# Andvance features (polls)
	def createPoll (self, title, choiceList, deadline):
		cid = self.produceTransaction ('dappforum.createPoll', [title, choiceList, deadline])
		return cid

	def listPolls (self):
		return self.consensusManager.jsonConsensusCall('dappforum.listPolls', [])['result']

	def getPollInfo (self, pollId):
		return self.consensusManager.jsonConsensusCall('dappforum.getPollInfo', [pollId])['result']		

	def vote (self, pollid, answer):
		cid = self.produceTransaction ('dappforum.vote', [pollid, answer])
		return cid

	# Andvance features (edit/delete)
	def getUserInfo (self, userAddress):
		return self.consensusManager.jsonConsensusCall('dappforum.getUserInfo', [userAddress])['result']

	def editPost (self, postId, title, body):
		cid = self.produceTransaction ('dappforum.editPost', [postId, title, body])
		return cid

	def editComment (self, commentId, comment):
		cid = self.produceTransaction ('dappforum.editComment', [commentId, comment])
		return cid

	def deletePost (self, postId):
		cid = self.produceTransaction ('dappforum.deletePost', [postId])
		return cid

	def deleteComment (self, commentId):
		cid = self.produceTransaction ('dappforum.deleteComment', [commentId])
		return cid

	def deletePoll (self, pollId):
		cid = self.produceTransaction ('dappforum.deletePoll', [pollId])
		return cid

	# Debug
	def isVoteInPoll(self, voteId, pollId):
		poll = self.getPollInfo (pollId)
		for vote in poll['votes']:
			if poll['votes'][vote]['vote_id'] == voteId:
				return True
		return False
