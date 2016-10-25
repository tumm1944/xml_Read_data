import numpy as NP
import xml.etree.ElementTree as ET
import gzip
import re
from scipy.stats.stats import pearsonr


Tags_tree = ET.parse(gzip.open('Tags.xml.gz', 'rb'))
Tags_root = Tags_tree.getroot()
tags_total=0
tags_count_total=0
tags_count = []


for Tags_child in Tags_root:
    #print Tags_child.tag, Tags_child.attrib
    tags_total = tags_total+1
    tags_count_total = tags_count_total + int(Tags_child.attrib['Count'])
    tags_count.append(int(Tags_child.attrib['Count']))
    #print tags_count[tags_total-1]

print tags_total, "= Total Tags"
print tags_count_total, " = Count Total"


tags_count = NP.array(tags_count)
sort_tags_count = NP.sort(tags_count)

print "5th most popular tag contains",sort_tags_count[-5], "posts"
print "5th most popular tag contains", float(sort_tags_count[-5])/tags_count_total, "=Fraction of Total posts"

for row in Tags_root.iter('row'):
    #print row.attrib['Count']
    if int(row.attrib['Count'])==sort_tags_count[-5]:
        print "5th mpst popular tag is ", row.attrib['TagName']

Score_questions = 0
posts_questions = 0
Score_answers = 0
posts_answers = 0

#question 2.2
Posts_tree = ET.parse(gzip.open('Posts.xml.gz', 'rb'))
Posts_root = Posts_tree.getroot()

for Posts_child in Posts_root:
    if Posts_child.attrib['PostTypeId']=="1":
        Score_questions=Score_questions+int(Posts_child.attrib['Score'])
        posts_questions=posts_questions+1
    elif Posts_child.attrib['PostTypeId']=="2":
        Score_answers=Score_answers+int(Posts_child.attrib['Score'])
        posts_answers=posts_answers+1

print "Average answer score",float(Score_answers)/posts_answers, "is", (float(Score_answers)/posts_answers)-(float(Score_questions)/posts_questions), "greater than average question score of",float(Score_questions)/posts_questions

#question 2.3


total_user_ids= []

Users_tree = ET.parse(gzip.open('Users.xml.gz', 'rb'))
Users_root = Users_tree.getroot()

for Users_child in Users_root:
    total_user_ids.append(int(Users_child.attrib['Id']))

print total_user_ids[-1]
total_users = total_user_ids[-1]
Users_reputation = NP.zeros([total_users,], dtype='int')
User_total_score_posts = NP.zeros([total_users,], dtype='int')

for Users_child in Users_root:
    Users_reputation[int(Users_child.attrib['Id'])-1] = int(Users_child.attrib['Reputation'])

for Posts_child in Posts_root:
    Value=Posts_child.attrib.get('OwnerUserId',123456)
    if Value==123456:
        print 'Owner User ID'
    else:
        #print Value
        User_total_score_posts[int(Value)-1] = User_total_score_posts[int(Value)-1] + int(Posts_child.attrib['Score'])


Q3_array = NP.column_stack((Users_reputation,User_total_score_posts))
nz = Q3_array[:,0] == 0
Q3_array_2 = Q3_array[nz == 0, :]

print pearsonr(Users_reputation,User_total_score_posts)
print pearsonr(Q3_array_2[:,0],Q3_array_2[:,1])


#OwnerUserId, Score in Posts and  Reputation, Id in Users

#question 2.4
# 1 posttypeid and 2 upmode for questions, 2 posttypeid and 2 upmode for answers
# PostId, VoteTypeId

Votes_tree = ET.parse(gzip.open('Votes.xml.gz', 'rb'))
Votes_root = Votes_tree.getroot()
max_post_id=int(Posts_child.attrib['Id'])
Post_type_id= NP.zeros([max_post_id,], dtype='int')
Votes_id= NP.zeros([max_post_id,], dtype='int')
votes_count_questions=0
votes_count_answers=0
count_questions=0
count_answers=0

for Posts_child in Posts_root:
    Post_type_id[(int(Posts_child.attrib['Id'])-1)]=int(Posts_child.attrib['PostTypeId'])
        
for Votes_child in Votes_root:
    if Votes_child.attrib['VoteTypeId']=='2':
        Votes_id[(int(Votes_child.attrib['PostId'])-1)]=Votes_id[(int(Votes_child.attrib['PostId'])-1)]+1
        
        
for index in range(max_post_id):
    if (Post_type_id[index]==1):
            votes_count_questions = votes_count_questions+ Votes_id[index]
            count_questions=count_questions+1
    elif (Post_type_id[index]==2):
        votes_count_answers = votes_count_answers+ Votes_id[index]
        count_answers=count_answers+1

print "Upvotes for answers are", float(votes_count_answers)/count_answers - float(votes_count_questions)/count_questions, "greater than upvotes for questions"
