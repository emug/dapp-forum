# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# Modified by Emanuele Muggiri.

import logging
import time

from contractvmd import config, dapp
from contractvmd.proto import Protocol
from contractvmd.chain.message import Message

logger = logging.getLogger(config.APP_NAME)

class ForumProto:
	DAPP_CODE = [ 0x74, 0x75 ]
	# Basic features (forum)
	METHOD_CREATE_POST = 0X01
	METHOD_COMMENT_POST = 0X02
	# Andvance features (polls)
	METHOD_CREATE_POLL = 0X03
	METHOD_VOTE = 0X04
	# Expert features (edit/delete)
	METHOD_EDIT_POST = 0X05
	METHOD_EDIT_COMMENT = 0X06
	METHOD_DELETE_POST = 0X07
	METHOD_DELETE_POLL = 0X08
	METHOD_DELETE_COMMENT = 0X09
	METHOD_LIST = [METHOD_CREATE_POST, METHOD_COMMENT_POST, METHOD_CREATE_POLL, METHOD_VOTE, METHOD_EDIT_POST, METHOD_EDIT_COMMENT, METHOD_DELETE_POST, METHOD_DELETE_POLL, METHOD_DELETE_COMMENT]


class ForumMessage (Message):
	# Basic features (forum)
	def createPost (title, body):
		m = ForumMessage()
		m.Title = title
		m.Body = body
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_CREATE_POST
		return m

	def commentPost (postId, comment):
		m = ForumMessage()
		m.PostId = postId
		m.Comment = comment
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_COMMENT_POST
		return m

	# Andvance features (polls)
	def createPoll (title, answerList, deadline):
		m = ForumMessage()
		m.Title = title
		m.AnswerList = answerList
		m.Deadline = deadline
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_CREATE_POLL
		return m

	def vote (pollId, answer):
		m = ForumMessage()
		m.PollId = pollId
		m.Answer = answer
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_VOTE
		return m

	# Expert features (edit/delete)
	def editPost (postId, title, body):
		m = ForumMessage()
		m.PostId = postId
		m.Title = title
		m.Body = body
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_EDIT_POST
		return m

	def editComment (commentId, comment):
		m = ForumMessage()
		m.CommentId = commentId
		m.Comment = comment
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_EDIT_COMMENT
		return m

	def deletePost (postId):
		m = ForumMessage()
		m.PostId = postId		
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELETE_POST
		return m

	def deleteComment (commentId):
		m = ForumMessage()
		m.CommentId = commentId		
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELETE_COMMENT
		return m

	def deletePoll (pollId):
		m = ForumMessage()
		m.PollId = pollId		
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELETE_POLL
		return m

	def toJSON (self):
		data = super (ForumMessage, self).toJSON ()
		
		# Basic features (forum)
		if self.Method == ForumProto.METHOD_CREATE_POST:
			data['title'] = self.Title
			data['body'] = self.Body
		elif self.Method == ForumProto.METHOD_COMMENT_POST:
			data['post_id'] = self.PostId
			data['comment'] = self.Comment
		# Andvance features (polls)
		elif self.Method == ForumProto.METHOD_CREATE_POLL:
			data['title'] = self.Title
			data['answer_list'] = self.AnswerList
			data['deadline'] = self.Deadline
		elif self.Method == ForumProto.METHOD_VOTE:
			data['poll_id'] = self.PollId
			data['answer'] = self.Answer
		# Expert features (edit/delete)
		elif self.Method == ForumProto.METHOD_EDIT_POST:
			data['post_id'] = self.PostId
			data['title'] = self.Title
			data['body'] = self.Body
		elif self.Method == ForumProto.METHOD_EDIT_COMMENT:
			data['comment_id'] = self.CommentId
			data['comment'] = self.Comment
		elif self.Method == ForumProto.METHOD_DELETE_POST:
			data['post_id'] = self.PostId
		elif self.Method == ForumProto.METHOD_DELETE_COMMENT:
			data['comment_id'] = self.CommentId
		elif self.Method == ForumProto.METHOD_DELETE_POLL:
			data['poll_id'] = self.PollId
		else:
			return None
		return data


class ForumAPI (dapp.API):
	def __init__ (self, vm, dht, api):
		self.api = api
		self.vm = vm
		self.dht = dht

		rpcmethods = {}

		# Basic features (forum)
		rpcmethods["createPost"] = {
			"call": self.method_createPost,
			"help": {"args": ["title", "body"], "return": {}}
		}
		
		rpcmethods["getPostInfo"] = {
			"call": self.method_getPostInfo,
			"help": {"args": ["post_id"], "return": {}}
		}

		rpcmethods["getCommentInfo"] = {
			"call": self.method_getCommentInfo,
			"help": {"args": ["comment_id"], "return": {}}
		}

		rpcmethods["listPost"] = {
			"call": self.method_listPost,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["listComment"] = {
			"call": self.method_listComment,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["commentPost"] = {
			"call": self.method_commentPost,
			"help": {"args": ["post_id", "comment"], "return": {}}
		}
		
		# Andvance features (polls)
		rpcmethods["createPoll"] = {
			"call": self.method_createPoll,
			"help": {"args": ["title", "answer_list", "deadline"], "return": {}}
		}

		rpcmethods["listPolls"] = {
			"call": self.method_listPolls,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["getPollInfo"] = {
			"call": self.method_getPollInfo,
			"help": {"args": ["poll_id"], "return": {}}
		}

		rpcmethods["vote"] = {
			"call": self.method_vote,
			"help": {"args": ["poll_id", "answer"], "return": {}}
		}

		# Expert features
		rpcmethods["getUserInfo"] = {
			"call": self.method_getUserInfo,
			"help": {"args": ['user_address'], "return": {}}
		}		
	
		rpcmethods["editPost"] = {
			"call": self.method_editPost,
			"help": {"args": ["post_id", "title", "body"], "return": {}}
		}

		rpcmethods["editComment"] = {
			"call": self.method_editComment,
			"help": {"args": ["comment_id", "comment"], "return": {}}
		}

		rpcmethods["deletePost"] = {
			"call": self.method_deletePost,
			"help": {"args": ["post_id"], "return": {}}
		}

		rpcmethods["deleteComment"] = {
			"call": self.method_deleteComment,
			"help": {"args": ["comment_id"], "return": {}}
		}

		rpcmethods["deletePoll"] = {
			"call": self.method_deletePoll,
			"help": {"args": ["poll_id"], "return": {}}
		}

		errors = { 'POST_NOT_FOUND': {'code': -2, 'message': 'Post not found'}, 'COMMENT_NOT_FOUND': {'code': -2, 'message': 'Comment not found'}, 'POLL_NOT_FOUND': {'code': -2, 'message': 'Poll not found'}, 'USER_NOT_FOUND': {'code': -2, 'message': 'User not found'} }

		super (ForumAPI, self).__init__(vm, dht, rpcmethods, errors)
	
	# Basic features (forum)
	def method_createPost (self, title, body):
		msg = ForumMessage.createPost(title, body)
		return self.createTransactionResponse (msg)

	def method_getPostInfo (self, postId):
		r = self.core.getPostInfo (postId)
		if r == None:
			return self.createErrorResponse ('POST_NOT_FOUND')
		else:
			return r
	
	def method_getCommentInfo (self, commentId):
		r = self.core.getCommentInfo (commentId)
		if r == None:
			return self.createErrorResponse ('COMMENT_NOT_FOUND')
		else:
			return r		

	def method_listPost (self):
		return self.core.listPost ()

	def method_listComment (self):
		return self.core.listComment ()

	def method_commentPost (self, postId, comment):
		msg = ForumMessage.commentPost(postId, comment)
		return self.createTransactionResponse (msg)	

	# Andvance features (polls)
	def method_createPoll (self, title, answerList, deadline):
		msg = ForumMessage.createPoll(title, answerList, deadline)
		return self.createTransactionResponse (msg)

	def method_listPolls (self):
		return self.core.listPolls ()

	def method_getPollInfo (self, pollId):
		r = self.core.getPollInfo (pollId)
		if r == None:
			return self.createErrorResponse ('POLL_NOT_FOUND')
		else:
			return r

	def method_vote (self, pollId, answer):
		msg = ForumMessage.vote (pollId, answer)
		return self.createTransactionResponse (msg)

	# Expert features
	def method_getUserInfo (self, userAddress):
		r = self.core.getUserInfo (userAddress)
		if r == None:
			return self.createErrorResponse ('USER_NOT_FOUND')
		else:
			return r

	def method_editPost (self, postId, title, body):
		msg = ForumMessage.editPost(postId, title, body)
		return self.createTransactionResponse (msg)

	def method_editComment (self, commentId, comment):
		msg = ForumMessage.editComment(commentId, comment)
		return self.createTransactionResponse (msg)

	def method_deletePost (self, postId):
		msg = ForumMessage.deletePost(postId)
		return self.createTransactionResponse (msg)

	def method_deleteComment (self, commentId):
		msg = ForumMessage.deleteComment(commentId)
		return self.createTransactionResponse (msg)

	def method_deletePoll (self, pollId):
		msg = ForumMessage.deletePoll(pollId)
		return self.createTransactionResponse (msg)

class ForumCore (dapp.Core):
	def __init__ (self, chain, database):
		# 'postids' list contains the list of the posts' IDs. Each post is stored in a DB row.
		database.init ('postids', [])

		# 'commentids' list contains the list of the comments' IDs. Each commet is stored in a DB row.
		# The comments are stored separatly from posts to simplify the "editComment()", "deleteComment()" and "getUserInfo()" methods
		database.init ('commentids', [])
		
		# 'pollids' list Contains the list of the polls' IDs. Each poll is stored in a DB row.
		database.init ('pollids', [])
		super (ForumCore, self).__init__ (chain, database)

	# Basic features (forum)
	def createPost (self, postId, author, title, body):
		self.database.listappend ('postids', postId)
		self.database.set(postId, {'author':author, 'title': title, 'body': body, 'comments': []})

	def listPost (self):
		return self.database.get('postids')

	def listComment (self):
		return self.database.get('commentids')

	def getPostInfo(self, postId):
		return self.database.get(postId)

	def getCommentInfo(self, commentId):
		return self.database.get(commentId)

	def commentPost (self, postId, commentId, author, comment):
		post = self.database.get(postId)
		if post != None:			
			newComment = {'post_id':postId, 'author':author, 'comment':comment}
			# stores the new comment into the db
			self.database.set(commentId, newComment)
			# stores the comment id into the 'commentids' list
			self.database.listappend('commentids', commentId)
			# adds the comment id into post
			post['comments'].append(commentId)
			self.database.set(postId, post)
		else:
			logger.pluginfo ('commentPost(): Post %s not found', postId)

	# Andvance features (polls)
	def createPoll (self, pollId, author, title, answerList, deadline):
		# initialize the answer list
		answers = {}		
		for answer in answerList:
			answers[answer] = {'votes': 0}
		# stores the new poll into the db
		self.database.set(pollId, {'poll_id':pollId, 'author':author, 'title': title, 'answers': answers, 'votes':{}, 'deadline': int(deadline)})
		# stores the poll id into the 'pollids' list
		self.database.listappend ('pollids', pollId)

	def listPolls (self):
		return self.database.get('pollids')

	def getPollInfo(self, pollId):
		return self.database.get (pollId)

	def vote (self, voteId, pollId, answer, voter):
		poll = self.database.get (pollId)
		if poll != None:
			if poll['deadline'] > int(time.time()):
				if answer in poll['answers']:
					if voter not in poll['votes']:						
						poll['answers'][answer]['votes'] += 1
						poll['votes'][voter] = {'vote_id':voteId, 'answer':answer}
						# updates poll
						self.database.set (pollId, poll)
						logger.pluginfo ('User %s voted', voter)
					else:
						logger.pluginfo ('vote(): Voter %s had already voted', voter)
				else:
					logger.pluginfo ('vote(): Invalid answer %s', answer)
			else:
				logger.pluginfo ('vote(): Poll %s is closed', pollId)
		else:
			logger.pluginfo ('vote(): Poll %s not found', pollId)

	# Expert features
	def getUserInfo (self, userAddress):
		result = {'posts':[], 'comments':[], 'polls':[]}
		for postid in self.database.get('postids'):
			if self.database.get(postid)['author'] == userAddress:
				result['posts'].append(postid)

		for commentid in self.database.get('commentids'):
			if self.database.get(commentid)['author'] == userAddress:
				result['comments'].append(commentid)

		for pollid in self.database.get('pollids'):
			if self.database.get(pollid)['author'] == userAddress:
				result['polls'].append(pollid)
		return result

	def editPost(self, userAddress, postId, title, body):
		post = self.database.get(postId)
		if post != None:
			if post['author'] == userAddress:
				# updates post
				post['title'] = title
				post['body'] = body
				self.database.set(postId, post)
			else:
				logger.pluginfo ('editPost(): Post %s is not owned by %s', postId, userAddress)
		else:
			logger.pluginfo ('editPost(): Post %s not found', postId)

	def editComment(self, userAddress, commentId, comment):
		c = self.database.get(commentId)
		if comment != None:
			if c['author'] == userAddress:
				#updates comment
				c['comment'] = comment
				self.database.set(commentId, c)
			else:
				logger.pluginfo ('editComment(): Comment %s is not owned by %s', commentId, userAddress)
		else:
			logger.pluginfo ('editComment(): Comment %s not found', commentId)	
	
	def deletePost(self, userAddress, postId):
		post = self.database.get(postId)
		if post != None:
			if post['author'] == userAddress:
				# Deletes all post's comments
				for commentId in post['comments']:
					self.database.delete(commentId)
					self.database.listremove('commentids', commentId)
				# Deletes post
				self.database.listremove('postids', postId)
				self.database.delete(postId)
			else:
				logger.pluginfo ('deletePost(): Post %s is not owned by %s', postId, userAddress)
		else:
			logger.pluginfo ('deletePost(): Post %s not found', postId)

	def deleteComment(self, userAddress, commentId):
		comment = self.database.get(commentId)
		if comment != None:
			if comment['author'] == userAddress:
				# Removes the comment from the post
				post = self.database.get(comment['post_id'])
				post['comments'].remove(commentId)
				self.database.set(comment['post_id'], post)
		
				# Deletes the commentId from the 'commentids' list
				self.database.listremove('commentids', commentId)

				# Deletes the comment from the DB
				self.database.delete(commentId)
			else:				
				logger.pluginfo ('deleteComment(): Comment %s is not owned by %s', commentId, userAddress)
		else:
			logger.pluginfo ('deleteComment(): Comment %s not found', commentId)


	def deletePoll(self, userAddress, pollId):
		poll = self.database.get(pollId)
		if poll != None:
			if poll['author'] == userAddress:
				self.database.listremove('pollids', pollId)
				self.database.delete(pollId)
			else:
				logger.pluginfo ('deletePoll(): Poll %s is not owned by %s', pollId, userAddress)
		else:
			logger.pluginfo ('deletePoll(): Poll %s not found', pollId)


class dappforum (dapp.Dapp):
	def __init__ (self, chain, db, dht, apimaster):
		self.core = ForumCore (chain, db)
		api = ForumAPI (self.core, dht, apimaster)		
		super (dappforum, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, api)
		

	def handleMessage (self, m):
		if m.Method == ForumProto.METHOD_CREATE_POST:
			logger.pluginfo ('Found new post %s: title:%s body:%s', m.Hash, m.Data['title'], m.Data['body'])
			self.core.createPost (m.Hash, m.Player, m.Data['title'], m.Data['body'])		
		elif m.Method == ForumProto.METHOD_COMMENT_POST:
			logger.pluginfo ('Found new comment %s: post_id:%s author:%s comment:%s', m.Hash, m.Data['post_id'], m.Player, m.Data['comment'])
			self.core.commentPost (m.Data['post_id'], m.Hash, m.Player, m.Data['comment'])
		elif m.Method == ForumProto.METHOD_CREATE_POLL:
			logger.pluginfo ('Found new poll %s: title:%s answer_list:%s deadline:%s', m.Hash, m.Data['title'], m.Data['answer_list'], m.Data['deadline'])
			self.core.createPoll (m.Hash, m.Player, m.Data['title'], m.Data['answer_list'], m.Data['deadline'])
		elif m.Method == ForumProto.METHOD_VOTE:
			logger.pluginfo ('Found new vote %s: from:%s poll:%s answer:%s', m.Hash, m.Player, m.Data['poll_id'], m.Data['answer'])
			self.core.vote (m.Hash, m.Data['poll_id'], m.Data['answer'], m.Player)
		elif m.Method == ForumProto.METHOD_EDIT_POST:
			logger.pluginfo ('Found new editPost request %s: from:%s post:%s title:%s body:%s', m.Hash, m.Player, m.Data['post_id'], m.Data['title'], m.Data['body'])
			self.core.editPost (m.Player, m.Data['post_id'], m.Data['title'], m.Data['body'])
		elif m.Method == ForumProto.METHOD_EDIT_COMMENT:
			logger.pluginfo ('Found new editComment request %s: from:%s comment:%s body:%s', m.Hash, m.Player, m.Data['comment_id'], m.Data['comment'])
			self.core.editComment (m.Player, m.Data['comment_id'], m.Data['comment'])
		elif m.Method == ForumProto.METHOD_DELETE_POST:
			logger.pluginfo ('Found new deletePost request %s: from:%s post:%s', m.Hash, m.Player, m.Data['post_id'])
			self.core.deletePost (m.Player, m.Data['post_id'])
		elif m.Method == ForumProto.METHOD_DELETE_COMMENT:
			logger.pluginfo ('Found new deleteComment request %s: from:%s comment:%s', m.Hash, m.Player, m.Data['comment_id'])
			self.core.deleteComment (m.Player, m.Data['comment_id'])
		elif m.Method == ForumProto.METHOD_DELETE_POLL:
			logger.pluginfo ('Found new deletePoll request %s: from:%s poll:%s', m.Hash, m.Player, m.Data['poll_id'])
			self.core.deletePoll (m.Player, m.Data['poll_id'])