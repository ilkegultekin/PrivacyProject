
import json
import graph
from os import listdir

class Policy:
    def __init__(self, _id, _context, _owner, thresholdVals, exceptions):
        self.polId = _id
        self.context = _context
        self.owner = _owner
        self.tstList = [('Family', thresholdVals[0]), ('Friend', thresholdVals[1]), ('Colleague', thresholdVals[2]), ('Manager', thresholdVals[3])]  # friend, family, colleague, manager
        self.excptList = exceptions
    
    def __str__(self):
        return self.polId + ": " + self.context + " - " + str(self.tstList) + " - " + str(self.excptList)
    
    __repr__ = __str__
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)
    
    def saveAsJson(self):
        fileHandler = open(self.owner + '/Policies/' + self.polId + '.json', 'w')
        json.dump(self, fileHandler, default=lambda o: o.__dict__, sort_keys=False, indent=2)

class Post:
    def __init__(self, _id, _context, _userList, _type, _content):
        self.id = _id
        self.context = _context
        self.userList = _userList
        self.type = _type
        self.content = _content
    
    def __str__(self):
        return self.content

# class User:
#     def __init__(self, _userId):
#         self.userId = _userId
#         self.password = _userId
#         self.policyList = []
#         
#     def addPolicy(self, _policy):
#         self.policyList.append(_policy)
#     
#     def __str__(self):
#         return self.userId
    
    __repr__ = __str__

class PrivacySystem():
    def __init__(self, networkArchitectureFile):
        self.networkGraph = graph.Graph(networkArchitectureFile)
        self.users = []
        self.posts = {}
        self.policies = {}
        self.loggedInUser = 'None'
        for vertex in self.networkGraph.vertices:
            self.users.append(vertex.id)
            self.posts[vertex.id] = []
            self.policies[vertex.id] = []
        
        self.addPredefinedPolicies()
    
    def addPredefinedPolicies(self):
        self.policies['Alice'].append(Policy('jobSearchPolicyAlice', 'job search', 'Alice', [3,2,3,4], []))
        self.policies['Bob'].append(Policy('jobSearchPolicyBob', 'job search', 'Bob', [2,3,5,4], ['Jaime']))
        #self.policies['Alice'].append(Policy('gossipPolicyAlice', 'office gossip', 'Alice', [3,1,4,5], []))
        #self.policies['Bob'].append(Policy('gossipPolicyBob', 'office gossip', 'Bob', [2,1,5,4], ['Dany']))
        
            
            
    def login(self, username, password):
        if username == 'Alice' and password == 'Alice':
            self.loggedInUser = 'Alice'
            return True
        elif username == 'Bob' and password == 'Bob':
            self.loggedInUser = 'Bob'
            return True
        else:
            return False
    
    def loginPrompt(self):
        numberOfUnsuccessfulTries = 0
        self.loggedIn = False
        while (not self.loggedIn and numberOfUnsuccessfulTries < 3):
            username = raw_input('Please enter your username\n')
            password = raw_input('Please enter your password\n')
            if self.login(username, password):
                print 'You are logged in as ' + self.loggedInUser
                self.loggedIn = True
            else:
                print 'Incorrect credentials' 
                numberOfUnsuccessfulTries += 1 
                if numberOfUnsuccessfulTries == 3:
                    print 'You have entered incorrect credentials three times. Program closing...'
                    self.closed = True
    
    def run(self):
        
        self.closed = False
        self.loginPrompt()
                
        while not self.closed:
            opt = raw_input('What would you like to do?\n1.Create New Post\n2.Enter a new policy\n3.Configure old policies\n4.Check conflicts\n5.Logout\n6.Close the program\n') 
            if opt == "1":
                postType = raw_input('Enter post type\n1.Status\n2.Photo\n')
                if postType == "1":
                    content = raw_input('Please enter your status update\n')
                    context = raw_input('Please enter the context of the post\n')
                    userList = raw_input('Please enter the affected users\n').split()
                    postId = raw_input('Please enter post id\n')
                    newPost = Post(postId, context, [self.loggedInUser] + userList, postType, content)
                if postType == 2:
                    content = raw_input('Please enter the photo url\n')
                    context = raw_input('Please enter the context of the post\n')
                    userList = raw_input('Please enter the affected users\n').split()
                    postId = raw_input('Please enter post id\n')
                    newPost = Post(postId, context, [self.loggedInUser] + userList, postType, content)
                     
                self.posts[self.loggedInUser].append(newPost)
                affectedUserList = newPost.userList
                
                decisionVector, conflictSet = self.detectConflict(newPost)
                print "Decision vector : "
                print decisionVector
                print
                print "Conflict set : "
                print conflictSet
                print
                conflictSetDecisions = self.resolveConflict(affectedUserList, conflictSet, self.loggedInUser, decisionVector)
                print "Conflict set final decisions : "
                print conflictSetDecisions
                print
                conflictSetDecisions = self.resolveConflictScenario1(affectedUserList, conflictSet, self.loggedInUser, decisionVector)
                print "Conflict set final decisions : "
                print conflictSetDecisions
                print
                conflictSetDecisions = self.resolveConflictScenario2(affectedUserList, conflictSet, self.loggedInUser, decisionVector)
                print "Conflict set final decisions : "
                print conflictSetDecisions
                print
                conflictSetDecisions = self.resolveConflictScenario3(affectedUserList, conflictSet, self.loggedInUser, decisionVector)
                print "Conflict set final decisions : "
                print conflictSetDecisions
                print
                conflictSetDecisions = self.resolveConflictScenario4(affectedUserList, conflictSet, self.loggedInUser, decisionVector)
                print "Conflict set final decisions : "
                print conflictSetDecisions
                self.saveConflict(content, context, postId, decisionVector, conflictSet, conflictSetDecisions)
                print
                
                
                
            elif opt == "2":    
                print 'Please enter your privacy policy'
                policyId = raw_input('Please enter a name for the policy\n')
                polContext = raw_input('Please enter the context of the policy\n')
                thresholdVals = raw_input('Please enter the minimum tie strength values for the following relationship types in the given order: Family Friend Colleague Manager\n').split()
                exceptions = raw_input('Please enter the name of the users who will be treated as exceptions\n').split()
                policy = Policy(policyId, polContext, self.loggedInUser, thresholdVals, exceptions)
                policy.saveAsJson()
                self.policies[self.loggedInUser].append(policy)
            elif opt == "3":
                userPols = self.policies[self.loggedInUser]
                print userPols
                print
                print
            elif opt == "4":
                fileList = listdir(self.loggedInUser + '/PreviousConflicts')
                if len(fileList) == 1:
                    print 'You have 1 new conflict'
                elif len(fileList) == 0:
                    print 'You have no new conflicts'
                else:
                    print 'You have ' + str(len(fileList)) + ' new conflict'
                for f in fileList:
                    self.printConflict(self.loggedInUser + '/PreviousConflicts/' + f)
                    print
                    print
            elif opt == "5":
                print 'You have logged out of the system'
                self.loginPrompt()
            elif opt == "6":
                print 'Program closing'
            self.closed = True
    
    def printConflict(self, fileInfo):
        fileHandle = open(fileInfo, 'r')
        lines = fileHandle.readlines()
        print 'date: ' + lines[0]
        print 'content: ' + lines[1]
        print 'context: ' + lines[2]
        print 'postOwner: ' + lines[3]
        print 'decisionVector: ' + lines[4]
        print 'conflictSet: ' + lines[5]
        print 'conflictSetDecisions: ' + lines[6]
                
    def saveConflict(self, content, context, postId, decisionVector, conflictSet, conflictSetDecisions):
        fileHandle = open('Bob/PreviousConflicts/' + postId + '.txt', 'w')
        fileHandle.write('%s\n', '10.05.2016')
        fileHandle.write('%s\n' % content)
        fileHandle.write('%s\n' % context)
        fileHandle.write('Alice\n')
        fileHandle.write(str(decisionVector))
        fileHandle.write('\n')
        fileHandle.write(str(conflictSet))
        fileHandle.write('\n')
        fileHandle.write(str(conflictSetDecisions))
        fileHandle.write('\n')
    
    def getRelationInfo(self, user1, user2):
        vertexEdgeMap = self.networkGraph.vertexEdgeMapping
        edges = vertexEdgeMap[user1]
        for edgeIndex in edges:
            edge = self.networkGraph.edges[edgeIndex]
            if edge.v2 == user2:
                return edge.tieStrength, edge.relationType
    
    def getRelevantPolicy(self, negUser, postContext):
        return [pol for pol in self.policies[negUser] if pol.context == postContext][0]
    
    def computeDecisionForSingleTargetUser(self, postContext, affectedUserList, targetUser):
        decisionDict = {}
        for negUser in affectedUserList:
            relevantPolicy = self.getRelevantPolicy(negUser, postContext)
            tieStrength, relationType = self.getRelationInfo(negUser, targetUser)
            relThreshold = int([threshold[1] for threshold in relevantPolicy.tstList if threshold[0] == relationType][0])
            if tieStrength >= relThreshold:
                dec = 1
                if targetUser in relevantPolicy.excptList:
                    dec = 0
            else:
                dec = 0
                if targetUser in relevantPolicy.excptList:
                    dec = 1
            decisionDict[negUser] = dec
        return decisionDict
    
    def detectConflict(self, post):
        affectedUserList = post.userList
        decisionVector = {}
        conflictSet = []
        for tarUser in self.users:
            if tarUser in affectedUserList:
                continue
            else:
                decisionDict = self.computeDecisionForSingleTargetUser(post.context, affectedUserList, tarUser)
                decisionVector[tarUser] = decisionDict
                if decisionDict.values()[0] != decisionDict.values()[1]:
                    conflictSet.append(tarUser)
        return decisionVector, conflictSet
        
    def estimateItemSensitivity(self, decisionVector, affectedUserList):
        itemSensitivity = {}
        for negUser in affectedUserList:
            thresholdVals = {'Family' : 5, 'Friend' : 5, 'Colleague' : 5, 'Manager' : 5}
            for tarUser in decisionVector.keys():
                if decisionVector[tarUser][negUser] == 0:
                    continue
                tieStrength, relationType = self.getRelationInfo(negUser, tarUser) 
                if thresholdVals[relationType] > tieStrength:
                    thresholdVals[relationType] = tieStrength
            curUserSen = float(sum(thresholdVals.values()))/4
            itemSensitivity[negUser] = curUserSen
        return itemSensitivity
    
    def computeMinTieStrForGrp(self, decisionVector, _relationType, negUser):
        minTieStr = 5
        for tarUser in decisionVector.keys():
            if decisionVector[tarUser][negUser] == 0:
                continue
            tieStrength, relationType = self.getRelationInfo(negUser, tarUser) 
            if relationType == _relationType and tieStrength < minTieStr:
                minTieStr = tieStrength
        return minTieStr
    
    def estimateTargetUserImportance(self, decisionVector, affectedUserList, conflictSet):
        importance = {}
        for tarUser in conflictSet:
            importance[tarUser] = {}
            for negUser in affectedUserList:
                tieStrength, relationType = self.getRelationInfo(negUser, tarUser)
                minTieStr = self.computeMinTieStrForGrp(decisionVector, relationType, negUser)
                importance[tarUser][negUser] = abs(minTieStr - tieStrength)
        return importance
    
    def estimateNegotiatingUserImportanceScenario1(self):
        #high tie strength, low success rate for Alice
        negUserImportance = {}
        negUserImportance['Alice'] = 5 * 0.2
        negUserImportance['Bob'] = 5 * 0.8
        return negUserImportance
    
    def estimateNegotiatingUserImportanceScenario2(self):
        #high tie strength, high success rate for Alice
        negUserImportance = {}
        negUserImportance['Alice'] = 5 * 0.8
        negUserImportance['Bob'] = 5 * 0.2
        return negUserImportance
    
    def estimateNegotiatingUserImportanceScenario3(self):
        #low tie strength, low success rate for Alice
        negUserImportance = {}
        negUserImportance['Alice'] = 2 * 0.3
        negUserImportance['Bob'] = 2 * 0.7
        return negUserImportance
    
    def estimateNegotiatingUserImportanceScenario4(self):
        #low tie strength, high success rate for Alice
        negUserImportance = {}
        negUserImportance['Alice'] = 2 * 0.7
        negUserImportance['Bob'] = 2 * 0.3
        return negUserImportance
    
    def estimateWillingness(self, conflictSet, itemSensitivity, importance, affectedUserList):
        maxVal = 5
        willingness = {}
        for tarUser in conflictSet:
            willingness[tarUser] = {}
            for negUser in affectedUserList:
                userItemSen = itemSensitivity[negUser]
                tarUserImportance = importance[tarUser][negUser]
                willingness[tarUser][negUser] = 0.5*(((maxVal - userItemSen)/float((maxVal + userItemSen))) + ((maxVal - tarUserImportance)/float((maxVal + tarUserImportance))))
        return willingness
    
    def estimateWillingnessModified(self, conflictSet, itemSensitivity, importance, affectedUserList, negUserImportanceDict):
        maxVal = 5
        willingness = {}
        for tarUser in conflictSet:
            willingness[tarUser] = {}
            for negUser in affectedUserList:
                userItemSen = itemSensitivity[negUser]
                tarUserImportance = importance[tarUser][negUser]
                negUserImportance = negUserImportanceDict[negUser]
                willingness[tarUser][negUser] = (1/float(3))*(((maxVal - userItemSen)/float((maxVal + userItemSen))) + ((maxVal - tarUserImportance)/float((maxVal + tarUserImportance))) + (negUserImportance/float(maxVal)))
        return willingness
                
    def resolveConflict(self, affectedUserList, conflictSet, postOwner, decisionVector):
        itemSensitivity = self.estimateItemSensitivity(decisionVector, affectedUserList)
        print "Item sensitivity for negotiating users : "
        print itemSensitivity
        print
        importance = self.estimateTargetUserImportance(decisionVector, affectedUserList, conflictSet)
        print "Target user importance values for negotiating users : "
        print importance
        print
        willingness = self.estimateWillingness(conflictSet, itemSensitivity, importance, affectedUserList)
        print "Willingness estimates : "
        print willingness
        print
        
        conflictSetDecisions = self.invokeRules(conflictSet, willingness, affectedUserList, decisionVector)
        return conflictSetDecisions
    
    def invokeRules(self, conflictSet, willingness, affectedUserList, decisionVector):
        conflictSetDecisions = {}
        for tarUser in conflictSet:
            print 'target user is %s' % tarUser
            willingnessVals = willingness[tarUser]
            if willingnessVals[affectedUserList[0]] > 0.5 and willingnessVals[affectedUserList[1]] > 0.5:
                print "Invoked rule: I do not mind positive"
                decision = 1
            elif willingnessVals[affectedUserList[0]] <= 0.5 and willingnessVals[affectedUserList[1]] <= 0.5:
                print "Invoked rule: I understand"
                decision = 0
            elif willingnessVals[affectedUserList[0]] > 0.5 and willingnessVals[affectedUserList[1]] <= 0.5:
                print "Invoked rule: I do not mind"
                decision = decisionVector[tarUser][affectedUserList[1]]
            elif willingnessVals[affectedUserList[1]] > 0.5 and willingnessVals[affectedUserList[0]] <= 0.5:
                print "Invoked rule: I do not mind"
                decision = decisionVector[tarUser][affectedUserList[0]]
            conflictSetDecisions[tarUser] = decision
        return conflictSetDecisions
                
    def resolveConflictScenario1(self, affectedUserList, conflictSet, postOwner, decisionVector):
        itemSensitivity = self.estimateItemSensitivity(decisionVector, affectedUserList)
        print "Item sensitivity for negotiating users : "
        print itemSensitivity
        print
        importance = self.estimateTargetUserImportance(decisionVector, affectedUserList, conflictSet)
        print "Target user importance values for negotiating users : "
        print importance
        print
        negUserImportanceDict = self.estimateNegotiatingUserImportanceScenario1()
        print "Scenario1: high tie strength between negotiating agents, low interaction success rate for Alice"
        print negUserImportanceDict
        
        willingness = self.estimateWillingnessModified(conflictSet, itemSensitivity, importance, affectedUserList, negUserImportanceDict)
        print "Willingness estimates : "
        print willingness
        print
        
        conflictSetDecisions = self.invokeRules(conflictSet, willingness, affectedUserList, decisionVector)
        
        return conflictSetDecisions
    
    def resolveConflictScenario2(self, affectedUserList, conflictSet, postOwner, decisionVector):
        itemSensitivity = self.estimateItemSensitivity(decisionVector, affectedUserList)
        print "Item sensitivity for negotiating users : "
        print itemSensitivity
        print
        importance = self.estimateTargetUserImportance(decisionVector, affectedUserList, conflictSet)
        print "Target user importance values for negotiating users : "
        print importance
        print
        negUserImportanceDict = self.estimateNegotiatingUserImportanceScenario2()
        print "Scenario1: high tie strength between negotiating agents, high interaction success rate for Alice \n"
        print negUserImportanceDict
        
        willingness = self.estimateWillingnessModified(conflictSet, itemSensitivity, importance, affectedUserList, negUserImportanceDict)
        print "Willingness estimates : "
        print willingness
        print
        
        conflictSetDecisions = self.invokeRules(conflictSet, willingness, affectedUserList, decisionVector)
        
        return conflictSetDecisions
    
    def resolveConflictScenario3(self, affectedUserList, conflictSet, postOwner, decisionVector):
        itemSensitivity = self.estimateItemSensitivity(decisionVector, affectedUserList)
        print "Item sensitivity for negotiating users : "
        print itemSensitivity
        print
        importance = self.estimateTargetUserImportance(decisionVector, affectedUserList, conflictSet)
        print "Target user importance values for negotiating users : "
        print importance
        print
        negUserImportanceDict = self.estimateNegotiatingUserImportanceScenario3()
        print "Scenario1: low tie strength between negotiating agents, low interaction success rate for Alice"
        print negUserImportanceDict
        
        willingness = self.estimateWillingnessModified(conflictSet, itemSensitivity, importance, affectedUserList, negUserImportanceDict)
        print "Willingness estimates : "
        print willingness
        print
        
        conflictSetDecisions = self.invokeRules(conflictSet, willingness, affectedUserList, decisionVector)
        
        return conflictSetDecisions
    
    def resolveConflictScenario4(self, affectedUserList, conflictSet, postOwner, decisionVector):
        itemSensitivity = self.estimateItemSensitivity(decisionVector, affectedUserList)
        print "Item sensitivity for negotiating users : "
        print itemSensitivity
        print
        importance = self.estimateTargetUserImportance(decisionVector, affectedUserList, conflictSet)
        print "Target user importance values for negotiating users : "
        print importance
        print
        negUserImportanceDict = self.estimateNegotiatingUserImportanceScenario4()
        print "Scenario1: low tie strength between negotiating agents, high interaction success rate for Alice"
        print negUserImportanceDict
        
        willingness = self.estimateWillingnessModified(conflictSet, itemSensitivity, importance, affectedUserList, negUserImportanceDict)
        print "Willingness estimates : "
        print willingness
        print
        
        conflictSetDecisions = self.invokeRules(conflictSet, willingness, affectedUserList, decisionVector)
        
        return conflictSetDecisions
            
        
            
                
        
            
                    

        
ps = PrivacySystem("../graph.txt")
ps.run()
# p = Policy('Alice', [('friend',2), ('family',3), ('colleague',4), ('manager',1)], ['Jon'])
# print p.toJSON()
    
    
    
