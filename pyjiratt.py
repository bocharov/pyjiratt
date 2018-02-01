#!/usr/bin/python3
import requests
import os
import argparse
import dateutil.parser

parser = argparse.ArgumentParser()
parser.add_argument("--since", default="startOfWeek()", help="date in YYYY-MM-DD format or JIRA date function")
parser.add_argument("--until", help="date in YYYY-MM-DD format or JIRA date function")
parser.add_argument("-v", action="store_true", help="increase output verbosity")
parser.add_argument("-vv", action="store_true", help="increase output verbosity more")
parser.add_argument("--jira-url", default=os.environ["JIRA_URL"], help="JIRA url, e.g. https://www.jira.com")
parser.add_argument("--jira-user", default=os.environ["JIRA_USER"], help="JIRA user name")
parser.add_argument("--jira-pass", default=os.environ["JIRA_PASS"], help="JIRA user password")
parser.add_argument("--assignee", default=os.environ["JIRA_ASSIGNEE"], help="JIRA assignee")
parser.add_argument("--max-results", default=1000, help="maximum of issues to fetch")
args = parser.parse_args()

requestsParams = {
    'startIndex': '0',
    'jql': 'assignee = %s AND timespent > 0 AND worklogDate >= %s' % (args.assignee, args.since),
    'fields': 'key,worklog,summary,reporter,link,status',
    'maxResults': args.max_results,
}
response = requests.get(args.jira_url + "rest/api/2/search", requestsParams, auth=(args.jira_user, args.jira_pass))

issues = response.json()['issues']
result = {}
for issue in issues:
    workLogs = issue['fields']['worklog']['worklogs']
    issueKey = issue['key']
    for worklog in workLogs:
        date = dateutil.parser.parse(worklog['started'])
        dateKey = date.strftime('%Y-%m-%d %a')

        if dateKey not in result:
            result[dateKey] = {
                'total': 0,
                'breakdown': {},
            }
        hours = int(worklog['timeSpentSeconds'] / 3600)
        result[dateKey]['total'] += hours
        result[dateKey]['breakdown'][issueKey] = {
            'hours': hours,
            'title': issue['fields']['summary'],
            'link': '%sbrowse/%s' % (args.jira_url, issueKey),
            'reporter': issue['fields']['reporter']['displayName'],
            'status': issue['fields']['status']['statusCategory']['name'],
        }

for key in sorted(result):
    if args.v:
        print("%s: %dh" % (key, result[key]['total']))
        for issueKey, issue in result[key]['breakdown'].items():
            print("    %s: %dh" % (issueKey, issue['hours']))
    elif args.vv:
        print("%s: %dh" % (key, result[key]['total']))
        for issueKey, issue in result[key]['breakdown'].items():
            print("  %s:" % issueKey)
            print("    Title: %s" % issue['title'])
            print("    Link: %s" % issue['link'])
            print("    Status: %s" % issue['status'])
            print("    Reporter: %s" % issue['reporter'])
            print("    Hours: %dh" % issue['hours'])
    else:
        print("%s: %dh" % (key, result[key]['total']))
