import datetime
import time
import sys
import boto.mturk.connection
import boto.mturk.question as mtq
import boto.mturk.qualification as mtqu

HOST = 'mechanicalturk.sandbox.amazonaws.com'
mt = boto.mturk.connection.MTurkConnection(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY,
                                           host=HOST)

image_url = 'http://i.imgur.com/ZiVaPei.jpg'
hits_count = 1

try:
    hits_count = int(sys.argv[1])
    image_url = sys.argv[2]
except:
    print 'Please provide the number of hits and an image url'
    sys.exit()

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
    duration=datetime.timedelta(seconds=15*60),
    )

hit_id = res[0].HITId
print 'Hit successfully published.'

word_stats = {}
expire_flag = True
while(expire_flag):
    time.sleep(15)
    print 'Check response..'
    assignments = mt.get_assignments(hit_id)
    if len(assignments) > 0:
        expire_flag = False
    for assignment in assignments:
        print "Answers of the worker %s" % assignment.WorkerId
        for question_form_answer in assignment.answers[0]:
            for word in question_form_answer.fields[0].split():
                if word in word_stats.keys():
                    word_stats[word] +=1
                else:
                    word_stats[word] = 0

print 'Successfully collected results.'
