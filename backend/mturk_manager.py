import datetime
import time
import boto.mturk.connection
import boto.mturk.question as mtq
import boto.mturk.qualification as mtqu

AWS_ACCESS_KEY_ID = 'AKIAIMKMN5ICEWOJFFAA'
AWS_SECRET_ACCESS_KEY = '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'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
mt = boto.mturk.connection.MTurkConnection(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY,
                                           host=HOST)

content = mtq.QuestionContent()
content.append_field('Text', 'Please tell us your first impression about the picture:')
image_link = '<img src="http://i.imgur.com/ZiVaPei.jpg" alt="target"></img>'
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
    max_assignments=1,
    approval_delay=datetime.timedelta(seconds=24*60*60),# auto-approve timeout
    duration=datetime.timedelta(seconds=15*60),# how fast the task is abandoned if not finished
    )

hit_id = res[0].HITId
print 'Hit successfully published.'

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
            print question_form_answer.fields[0]

print 'Successfully collected results.'
