#!/usr/bin/python
import datetime
import os

# Revision spec, directory name.
revisions = [('3', '2005-07-13')]
rev_date = [2005, 7, 13]
#stop = datetime.date.today()
stop = datetime.date(2011, 10, 26)

# Calculate date strings for every six months after revision 3.
while True:
    rev_date[1] += 6
    if rev_date[1] > 12:
        rev_date[1] -= 12
        rev_date[0] += 1
    if datetime.date(*rev_date) > stop:
        break
    date_str = datetime.date(*rev_date).strftime('%Y-%m-%d')
    revisions.append(('{%s}' % date_str, date_str))
 
# Add stopping date as the last revision to grab.
date_str = stop.strftime('%Y-%m-%d')
revisions.append(('{%s}' % date_str, date_str))

print 'revisions to grab: %s' % revisions
#raise Exception()

for revision, directory in revisions:
    if not os.path.exists(directory):
        cmd = 'svn export -r %s http://code.djangoproject.com/svn/django/trunk/ %s' % (revision, directory)
        print 'running command: %s' % cmd
        os.system(cmd)


