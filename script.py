import csv
import json
import time
import tweepy


# You must use Python 2.7.x

# 1 point
def loadKeys(key_file):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
    json_data = open(key_file)
    data = json.load(json_data)
    return str(data['api_key']),str(data['api_secret']),str(data['token']),str(data['token_secret'])

# 4 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    user = api.get_user(root_user)
    #print user.screen_name
    #print user.followers_count
    
    primary_friends = []
    for friend in user.friends()[0:no_of_friends]:
        primary_friends.append((root_user,str(friend.screen_name)))
    # Add code here to populate primary_friends
    return primary_friends

# 4 points
def getNextLevelFriends(api, users_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each user in users_list
    # rtype: list containing entries in the form of a tuple (user, friend)
    #users_list[i]
    users_list=[k for j,k in users_list]
    next_level_friends = []
    for i in range(len(users_list)):
        next_level_friends=next_level_friends+getPrimaryFriends(api,users_list[i],no_of_friends)
        time.sleep(65)
    # Add code here to populate next_level_friends
    return next_level_friends

# 4 points
def getNextLevelFollowers(api, users_list, no_of_followers):
    users_list=[k for j,k in users_list]
    # TODO: implement the method for fetching 'no_of_followers' followers for each user in users_list
    # rtype: list containing entries in the form of a tuple (follower, user)    
    next_level_followers = []
    for i in range(len(users_list)): 
        for follower in api.followers_ids(users_list[i])[0:no_of_followers]:
            next_level_followers.append((str(api.get_user(follower).screen_name),users_list[i]))
        time.sleep(65)
    # Add code here to populate next_level_followers
    return next_level_followers

# 3 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the 
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends. 
       
    all_edges = [] 
    list_tup1=getPrimaryFriends(api, root_user, no_of_neighbours)
    list_tup2=getNextLevelFriends(api, list_tup1, no_of_neighbours)
    list_tup3=getNextLevelFollowers(api, list_tup1, no_of_neighbours)
    all_edges=list_tup1+list_tup2+list_tup3
    #Add code here to populate all_edges
    return all_edges


# 2 points
    '''
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file,'wb') as resultFile:
        wr = csv.writer(resultFile)
        for i in data:
            wr.writerows(i)
    #pass

'''

def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)



"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)
    

if __name__ == '__main__':
    testSubmission()


