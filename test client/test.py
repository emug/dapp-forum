#!/usr/bin/python3
## Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# Modified by Emanuele Muggiri.

from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from dappforum import ForumManager
from colorlog import ColoredFormatter
import sys
import time
import os
import logging

SLEEP_DELAY = 10 # wait delay
A_USER_ADDRESS = 'mnHdrckZC15D1zHhMs5JnwicUbWkAWCqm6'
B_USER_ADDRESS = 'mi7EQnp3oiksXqTJWJEXEKDHL6b6RtSUTe'
POLL_DEADLINE = 1456617600

# Stop ConsensusManager logger
loggerCon = logging.getLogger('libcontractvm')
loggerCon.disabled = True

# Sets new logger
logger = logging.getLogger('test')
logger.setLevel('DEBUG')
formatter = ColoredFormatter(
	'%(log_color)s[%(asctime)s] %(message)s',
	datefmt='%d-%m-%Y %X',
	reset=True,
	log_colors = {
		'DEBUG':	'green',
		'PLUGINFO': 'purple',
		'INFO':	 'white',
		'WARNING':  'yellow',
		'ERROR':	'red',
		'CRITICAL': 'red',
	},
	style = '%'
)
stream = logging.StreamHandler ()
stream.setFormatter (formatter)
logger.addHandler (stream)

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

# Wallets A and B
walletA = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
walletB = WalletExplorer.WalletExplorer (wallet_file='B.wallet')

# Forum managers for users A and B
forumManA = ForumManager.ForumManager (consMan, wallet=walletA)
forumManB = ForumManager.ForumManager (consMan, wallet=walletB)

# returns the string representation of a post
def postToStr(p):
	msg = '\t author:' + p['author'] + '\n\t title:' + p['title'] + '\n\t body:' + p['body']
	msg += '\n\t comments:'
	comments = p['comments']
	for commentId in p['comments']:
			c = forumManA.getCommentInfo (commentId)
			msg += '\n\t\t id:' + commentId + '\n\t\t\t author:' + c['author'] + '\n\t\t\t comment:' + c['comment']
	return msg

# returns the string representation of a poll
def pollToStr (p):
	msg = '\t author:' + p['author'] + '\n\t title:' + p['title'] + '\n\t deadline:' + str(p['deadline'])
	if int(time.time()) < p['deadline']:
		msg += '\n\t state: OPEN'
	else:
		msg += '\n\t state: CLOSE'
	msg += '\t\n answers:'
	for answer in p['answers'].keys():
		msg += '\n\t\t ' + answer + ': ' + str(p['answers'][answer]['votes'])
	msg += '\n\t Votes:'
	for vote in p['votes'].keys():
		msg += '\n\t\t voter:' + vote + ' vote_id:' + p['votes'][vote]['vote_id'] + ' answer:' + str(p['votes'][vote]['answer'])
	return msg

# prints the list of user's posts, comments and polls ids
def printUserInfo(userInfo):
	logger.debug('post:[ "%s" ] comments:[ "%s" ] polls:[ "%s" ]', '", "'.join(userInfo['posts']), '", "'.join(userInfo['comments']), '", "'.join(userInfo['polls']))

# test function
def test():
# Basic features test
	logger.debug ('Basic Features Test Started')

	# A: postid = createPost ('Hello post', 'Post di test')
	postid = forumManA.createPost ('Hello post', 'Post di test')
	logger.debug('A -> CREATE_POST -> %s', postid)

	# ~: listPost() As long as the post (postid) appears
	logger.info('wait post %s', postid)
	while(postid not in forumManA.listPost()):
		time.sleep(SLEEP_DELAY)
	posts = forumManA.listPost ()
	logger.debug ('A -> LIST_POST --> [ "%s" ]', '", "'.join(posts))

	# A: commid = commentPost (postid, 'This is a comment')
	commid = forumManA.commentPost (postid, 'This is a comment')
	logger.debug ('A -> COMMENT_POST %s -> %s', postid, commid)

	# ~: getPostInfo (postid)  As long as the comment (commid) appears
	logger.info ('wait comment %s', commid)
	while(commid not in forumManA.listComment()):
		time.sleep(SLEEP_DELAY)
	post = forumManA.getPostInfo(postid)
	logger.debug ('A -> GET_POST_INFO -> %s \n%s', postid, postToStr(post))

	# B: postid2 = createPost (‘Hello post 2’, ‘Post di test2’)	
	postid2 = forumManB.createPost ('Hello post 2', 'Post di test2')
	logger.debug ('B -> CREATE_POST -> %s', postid2)

	# B: commid2 = commentPost (postid, ‘This is a comment of B’)
	commid2 = forumManB.commentPost (postid, 'This is a comment of B')
	logger.debug ('B -> COMMENT_POST %s -> %s', postid, commid2)

	# ~: getPostInfo (postid) As long as the comment (commid2) appears
	logger.info ('wait comment %s', commid2)
	while(commid2 not in forumManA.listComment()):
		time.sleep(SLEEP_DELAY)
	post = forumManA.getPostInfo(postid)
	logger.debug ('A -> GET_POST_INFO -> %s \n%s', postid, postToStr(post))

	logger.debug ('Basic Features Test Ended')

# Advance features test
	logger.debug ('Advanced Features Test Started')

	# A: pollid = createPoll ('Title', ['answer1', 'answer2', …], deadline)
	pollid = forumManA.createPoll('Title', ['answer1', 'answer2', 'answer3'], POLL_DEADLINE)
	logger.debug('A -> CREATE_POLL -> %s', pollid)

	# ~: listPolls () As long as the poll (pollid) appears
	logger.info('wait poll %s', pollid)
	while( pollid not in forumManA.listPolls () ):
		time.sleep(SLEEP_DELAY)
	polls = forumManA.listPolls ()
	logger.debug('A -> LIST_POLLS -> [ "%s" ]', '", "'.join(polls))

	# A: voteid1 = vote (pollid, ‘answer1)
	voteid1 = forumManA.vote (pollid, 'answer1')
	logger.debug('A -> VOTE_POLL %s -> %s', pollid, voteid1)
	
	# wait for first vote. (Contractvm process the transactions in the same block in reverse time order so, without the wait 
	# voteid2 could be accepted prior voteid1)
	logger.info('wait vote %s', voteid1)
	while( not forumManB.isVoteInPoll(voteid1, pollid) ):
		time.sleep(SLEEP_DELAY)

	# A: voteid2 = vote (pollid, ‘answer2’) This should fail, double vote
	voteid2 = forumManA.vote (pollid, 'answer1')
	logger.debug('A -> VOTE_POLL %s -> %s', pollid, voteid2)

	# ~: getPollInfo (pollid) As long as the vote (voteid1) appears
	logger.info('wait vote %s', voteid1)
	while( not forumManA.isVoteInPoll(voteid1, pollid) ):
		time.sleep(SLEEP_DELAY)
	poll = forumManA.getPollInfo(pollid)
	logger.debug('A -> GET_POLL_INFO -> %s \n%s', pollid, pollToStr(poll))
	
	# B: voteid3 = vote (pollid, ‘answer2’)
	voteid3 = forumManB.vote (pollid, 'answer2')
	logger.debug('B -> VOTE_POLL %s -> %s', pollid, voteid3)

	# ~: getPollInfo (pollid) As long as the vote (voteid3) appears
	logger.info('wait vote %s', voteid3)
	while( not forumManB.isVoteInPoll(voteid3, pollid) ):
		time.sleep(SLEEP_DELAY)
	poll = forumManB.getPollInfo(pollid)
	logger.debug ('B -> GET_POLL_INFO -> %s \n%s', pollid, pollToStr(poll))

	# B: pollid2 = createPoll (‘Title’, [‘answer1’, ‘answer2’, …], deadline)
	pollid2 = forumManB.createPoll('Title', ['answer1', 'answer2', 'answer3, answer4'], POLL_DEADLINE)
	logger.debug('B -> CREATE_POLL -> %s', pollid2)

	# ~: listPolls () As long as the poll (pollid2) appears
	logger.info('wait poll %s', pollid2)
	while( pollid2 not in forumManB.listPolls () ):
		time.sleep(SLEEP_DELAY)
	polls = forumManB.listPolls ()
	logger.debug('B -> LIST_POLLS -> [ "%s" ]', '", "'.join(polls))

	logger.debug ('Advance Features Test Ended')

# Expert features test
	logger.debug ('Expert Features Test Started')

	# ~: getUserInfo (AUserAddress)
	userInfo = forumManA.getUserInfo(A_USER_ADDRESS)
	logger.debug('A -> GET_USER_INFO -> [ "%s" ]', A_USER_ADDRESS)
	printUserInfo(userInfo)

	# B: editComment (commid, 'New comment 1 message')  This should fail, commid is owned by A
	forumManB.editComment (commid, 'New comment 1 message')
	logger.debug('B -> EDIT_COMMENT -> [ "%s" ]', commid)
	
	# A: editComment (commid, ‘New comment 2 message’)
	forumManA.editComment (commid, 'New comment 2 message')
	logger.debug('A -> EDIT_COMMENT -> [ "%s" ]', commid)

	# B: editPost (postid, 'New hello post', 'New message!')  This should fail, postid is owned by A
	forumManB.editPost (postid, 'New hello post', 'New message!')
	logger.debug('B -> EDIT_POST -> [ "%s" ]', postid)

	# A: editPost (postid, ‘New hello post A’, ‘New message!’)
	forumManA.editPost (postid, 'New hello post A', 'New message!')
	logger.debug('A -> EDIT_POST -> [ "%s" ]', postid)

	# ~: listPost () As long as the post (postid) appears with the changed title
	logger.info('wait post %s update', postid)
	post = forumManA.getPostInfo(postid)
	while(post['title'] != 'New hello post A'):
		time.sleep(SLEEP_DELAY)
		post = forumManA.getPostInfo(postid)
	
	posts = forumManA.listPost ()
	logger.debug ('A -> LIST_POST --> [ "%s" ]', '", "'.join(posts))

	# A: deleteComment (commid)
	forumManA.deleteComment(commid)
	logger.debug ('A -> DELETE_COMMENT --> [ "%s" ]', commid)

	# B: commid3 = commentPost (postid, 'This is a new comment') 
	commid3 = forumManB.commentPost (postid, 'This is a new comment')
	logger.debug ('B -> COMMENT_POST %s -> %s', postid, commid3)

	# A: getPostInfo (postid)  As long as the comment (commid3) appears
	logger.info ('wait comment %s', commid3)
	while(commid3 not in forumManA.listComment()):
		time.sleep(SLEEP_DELAY)
	post = forumManA.getPostInfo(postid)
	logger.debug ('A -> GET_POST_INFO -> %s \n%s', postid, postToStr(post))

	# A: deleteComment (commid3)  This should fail, commid2 is owned by B
	forumManA.deleteComment(commid3)
	logger.debug ('A -> DELETE_COMMENT --> [ "%s" ]', commid3)

	# B: deleteComment (commid3)
	forumManB.deleteComment(commid3)
	logger.debug ('B -> DELETE_COMMENT --> [ "%s" ]', commid3)

	# ~: getPostInfo (postid)  As long as the comment (commid3) disappears
	logger.info ('wait deleteComment %s', commid3)
	while(commid3 in forumManA.listComment()):
		time.sleep(SLEEP_DELAY)
	post = forumManA.getPostInfo(postid)
	logger.debug ('A -> GET_POST_INFO -> %s \n%s', postid, postToStr(post))

	# B: deletePost (postid)  This should fail, postid is owned by A
	forumManB.deletePost(postid)
	logger.debug ('B -> DELETE_POST -> [ %s ]', postid)

	# A: deletePost (postid)
	forumManA.deletePost(postid)
	logger.debug ('A -> DELETE_POST -> [ %s ]', postid)

	# ~: listPost ()  As long as the post (postid) disappears
	logger.info ('wait deletePost %s', postid)
	while(postid in forumManA.listPost()):
		time.sleep(SLEEP_DELAY)
	posts = forumManA.listPost ()
	logger.debug ('A -> LIST_POST --> [ "%s" ]', '", "'.join(posts))

	# B: deletePoll (pollid2)
	forumManB.deletePoll(pollid2)
	logger.debug ('B -> DELETE_POLL -> [ %s ]', pollid2)

	# ~: listPoll ()  As long as the poll (pollid2) disappears
	logger.info ('wait deletePost %s', pollid2)
	while(pollid2 in forumManA.listPolls()):
		time.sleep(SLEEP_DELAY)
	polls = forumManB.listPolls ()
	logger.debug('A -> LIST_POLLS -> [ "%s" ]', '", "'.join(polls))

	# ~: getUserInfo (BUseraddress)
	userInfo = forumManA.getUserInfo(B_USER_ADDRESS)
	logger.debug('A -> GET_USER_INFO -> [ "%s" ]', B_USER_ADDRESS)
	printUserInfo(userInfo)

	# ~: getUserInfo (AUserAddress)
	userInfo = forumManA.getUserInfo(A_USER_ADDRESS)
	logger.debug('A -> GET_USER_INFO -> [ "%s" ]', A_USER_ADDRESS)
	printUserInfo(userInfo)

	logger.debug ('Expert Features Test Ended')

os.system ('clear')
print ('Forum test script')
test()