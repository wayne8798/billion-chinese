import datetime
import time
import sys
import string
from nltk import PorterStemmer as psmer
import boto.mturk.connection
import boto.mturk.question as mtq
import boto.mturk.qualification as mtqu

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
HOST = 'mechanicalturk.amazonaws.com'
# sandbox host
# HOST = 'mechanicalturk.sandbox.amazonaws.com'

image_url = 'http://i.imgur.com/ZiVaPei.jpg'
hits_count = 20

try:
    hits_count = int(sys.argv[1])
    image_url = sys.argv[2]
    AWS_ACCESS_KEY_ID = sys.argv[3]
    AWS_SECRET_ACCESS_KEY = sys.argv[4]
except:
    print 'Please provide the number of hits, image url and AWS credentials'
    sys.exit()

mt = boto.mturk.connection.MTurkConnection(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY,
                                           host=HOST)

text_description = ''' Please use 3 words separated by space to describe
the impression this picture gives to you.
'''
image_link = '<img src="' + image_url + '" alt="target"></img>'
content = mtq.QuestionContent()
content.append_field('Text', text_description)
content.append(mtq.FormattedContent(image_link))

question = mtq.Question(
    'response',
    content = content,
    answer_spec = mtq.AnswerSpecification(mtq.FreeTextAnswer()),
    is_required = True,
    )
 
qualifications = mtqu.Qualifications()
qualifications.add(mtqu.PercentAssignmentsApprovedRequirement('GreaterThanOrEqualTo', 75))

res = mt.create_hit(
    questions=[question],
    qualifications=qualifications,
    title = 'Image Impression Survey',
    description = 'Tell us your thought about the provided image',
    keywords='image, impression',
    reward=mt.get_price_as_price(0.05),
    max_assignments=hits_count,
    approval_delay=datetime.timedelta(seconds=24*60*60),
    duration=datetime.timedelta(seconds=10*60),
    )

hit_id = res[0].HITId
print 'Hit successfully published.'

word_stats = {}
expire_flag = True
time_count = 0
while(expire_flag):
    time.sleep(60)
    time_count += 1
    print str(time_count) + ' mins passed..'
    hits = mt.get_reviewable_hits(sort_direction='Descending')
    for hit in hits:
        if hit.HITId == hit_id:
            print 'Task finished.'
            expire_flag = False
            assignments = mt.get_assignments(hit_id)
            for assignment in assignments:
                for question_form_answer in assignment.answers[0]:
                    answer = question_form_answer.fields[0]
                    for p in string.punctuation:
                        answer = answer.replace(p, ' ')
                    for word in answer.lower().split():
                        stemmed_word = psmer().stem_word(word)
                        if stemmed_word in word_stats.keys():
                            word_stats[stemmed_word] += 1
                        else:
                            word_stats[stemmed_word] = 1

print 'Successfully collected results.'
print word_stats
