'''
Created on Nov 4, 2011

@author: QualityCan
'''

# For each ticket list it's creating timestamp (14), and columns giving its current state

#Time to close
#Created (14)
#Whatever vs Time (14)

import math, time, csv, sys, xml, datetime

from xmlrpc import client

# 13 July 2005, 13 January 2006, ..., 13 July 2011, 26 October 2011
def main():
    s = client.ServerProxy('https://QualityCan:)G(&G3gH)&03857@code.djangoproject.com/login/rpc')
    ticket_metrics(s)
    #wiki_metrics(s)
    print('Done')
    
def ticket_metrics(s):
    print('Writing ticket metrics...')
    
    date_tuples = [\
        [2005,7,13],[2006,1,13],[2006,7,13],[2007,1,13],[2007,7,13],\
        [2008,1,13],[2008,7,13],[2009,1,13],[2009,7,13],[2010,1,13],\
        [2010,7,13],[2011,1,13],[2011,7,13],[2011,10,26]]
    last = datetime.date(*date_tuples[len(date_tuples) - 1])
    prev = last - datetime.timedelta(weeks=1)
    max_ticket = 13000#max(s.ticket.query('created={0}..{1}'.format(prev, last)))
    
    # Build database of all tickets
    ticket_db = []
    change_db = {}
    for ticket_idx in range(13000, max_ticket + 1):
        print('Processing ticket {0} of {1}'.format(ticket_idx, max_ticket))
        try:
            ticket = s.ticket.get(ticket_idx)
            change = s.ticket.changeLog(ticket_idx)
            ticket_db.append(ticket)
            change_db[ticket_idx] = change
        except (client.Fault, xml.parsers.expat.ExpatError):
            pass
    
    # Write header
    csv_rows = []
    csv_row = ['Ticket','Creat','Mod','Closd','Diff',\
        'Type','Stat','Sever','Resol','Compon','Intrv']
    for i in date_tuples:
        csv_row.append(datetime.date(*i))
        csv_row.append('Type')
        csv_row.append('Stat')
        csv_row.append('Sever')
        csv_row.append('Resol')
        csv_row.append('Compon')
    csv_rows.append(csv_row)
    # Write raw ticket data
    for ticket in ticket_db:
        csv_row = []
        # First easy cols
        csv_row.append(ticket[0])
        csv_row.append(datetime.date(*ticket[1].timetuple()[:3]))
        csv_row.append(datetime.date(*ticket[2].timetuple()[:3]))
        # Closed, and diff: the time it was last closed minus creation
        created = datetime.datetime(*ticket[1].timetuple()[:6])
        modified = None
        for change_date_idx in range(len(change_db[ticket[0]])-1,-1,-1):
            if 'status' in change_db[ticket[0]][change_date_idx][1:]:
                status_idx = change_db[ticket[0]][change_date_idx][1:].index('status')
                if 'closed' == change_db[ticket[0]][change_date_idx][1:][status_idx + 2]:
                    modified = change_db[ticket[0]][change_date_idx][0]
                    modified = datetime.datetime(*modified.timetuple()[:6])
                    break
        if modified:
            csv_row.append(modified.date())
            csv_row.append((modified - created).days)
        else:
            csv_row.append('')
            csv_row.append('')
        # Write easy cols
        csv_row.append(ticket[3]['type'])
        csv_row.append(ticket[3]['status'])
        csv_row.append(ticket[3]['severity'])
        csv_row.append(ticket[3]['resolution'])
        csv_row.append(ticket[3]['component'])
        # Which time interval the ticket belongs
        for i in range(len(date_tuples) - 1):
            strt_date = datetime.date(*date_tuples[i])
            stop_date = datetime.date(*date_tuples[i + 1])
            if strt_date <= created.date() < stop_date:
                csv_row.append(i + 1)
                break
        else:
            csv_row.append('')
        # The ticket's state at each time interval
        for i in date_tuples:
            state_type = ticket[3]['type']
            state_status = ticket[3]['status']
            state_severity = ticket[3]['severity']
            state_resolution = ticket[3]['resolution']
            state_component = ticket[3]['component']
            state_date = datetime.date(*i)
            for change_date_idx in range(len(change_db[ticket[0]])-1,-1,-1):
                rev_date = change_db[ticket[0]][change_date_idx][0]
                rev_date = datetime.date(*ticket[2].timetuple()[:3])
                if rev_date < state_date:
                    break
                if 'type' in change_db[ticket[0]][change_date_idx][1:]:
                    idx = change_db[ticket[0]][change_date_idx][1:].index('type')
                    state_type = change_db[ticket[0]][change_date_idx][1:][idx + 1]
                if 'status' in change_db[ticket[0]][change_date_idx][1:]:
                    idx = change_db[ticket[0]][change_date_idx][1:].index('status')
                    state_status = change_db[ticket[0]][change_date_idx][1:][idx + 1]
                if 'severity' in change_db[ticket[0]][change_date_idx][1:]:
                    idx = change_db[ticket[0]][change_date_idx][1:].index('severity')
                    state_severity = change_db[ticket[0]][change_date_idx][1:][idx + 1]
                if 'resolution' in change_db[ticket[0]][change_date_idx][1:]:
                    idx = change_db[ticket[0]][change_date_idx][1:].index('resolution')
                    state_resolution = change_db[ticket[0]][change_date_idx][1:][idx + 1]
                if 'component' in change_db[ticket[0]][change_date_idx][1:]:
                    idx = change_db[ticket[0]][change_date_idx][1:].index('component')
                    state_component = change_db[ticket[0]][change_date_idx][1:][idx + 1]
            created = datetime.date(*ticket[1].timetuple()[:3])
            if created <= state_date:
                csv_row.append('')
                csv_row.append(state_type)
                csv_row.append(state_status)
                csv_row.append(state_severity)
                csv_row.append(state_resolution)
                csv_row.append(state_component)
            else:
                csv_row.append('')
                csv_row.append('')
                csv_row.append('')
                csv_row.append('')
                csv_row.append('')
                csv_row.append('')
        csv_rows.append(csv_row)
    write_csv('metrics_ticket_test.csv', csv_rows)

def wiki_metrics(s):
    print('Writing wiki metrics...')
    csv_rows = [['Name', '#Attach', '#Versns']]
    max_versions = 1
    pages = s.wiki.getAllPages()
    for index in range(245, len(pages)):
        print('Processing "{0}" (page {1} of {2})'.format(\
            pages[index], index + 1, len(pages)))
        page_name = pages[index]
        attachment_count = len(s.wiki.listAttachments(page_name))
        version_count = s.wiki.getPageInfo(page_name)['version']
        max_versions = max(max_versions, version_count)
        csv_row = [page_name, attachment_count, version_count]
        for i in range(1, version_count + 1):
            info = s.wiki.getPageInfo(page_name, i)
            version = info['version']
            last_modified = info['lastModified']
            l_m_dt = datetime.strptime(last_modified.value, "%Y%m%dT%H:%M:%S")
            l_m_str = l_m_dt.strftime("%d/%m/%Y")
            try:
                content_length = len(s.wiki.getPageVersion(page_name, i))
            except xml.parsers.expat.ExpatError:
                content_length = ''
            csv_row.append('v{0}'.format(version))
            csv_row.append(l_m_str)
            csv_row.append(content_length)
        csv_rows.append(csv_row)
    # Finish writing header
    for i in range(max_versions):
        csv_rows[0].extend(['', 'L.Mod.', '#Chars'])
    write_csv('metrics_wiki.csv', csv_rows)

def write_csv(name, csv_rows):
    with open(name, 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerows(csv_rows)

if __name__ == '__main__':
    main()
