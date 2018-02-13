#!/usr/bin/env python3
import requests
import os
import argparse
import dateutil.parser
import datetime


def start_of_week() -> datetime.date:
    now = datetime.datetime.now()
    return datetime.date(now.year, now.month, now.day - now.weekday())


def start_of_month() -> datetime.date:
    now = datetime.datetime.now()
    return datetime.date(now.year, now.month, 1)


parser = argparse.ArgumentParser()
parser.add_argument("--since", default="start_of_week()", help="date in YYYY-MM-DD format or date function")
parser.add_argument("--until", help="date in YYYY-MM-DD format or JIRA date function")
parser.add_argument("-v", action="store_true", help="increase output verbosity")
parser.add_argument("-vv", action="store_true", help="increase output verbosity more")
parser.add_argument("--jira-url", default=os.environ["JIRA_URL"], help="JIRA url, e.g. https://www.jira.com")
parser.add_argument("--jira-user", default=os.environ["JIRA_USER"], help="JIRA user name")
parser.add_argument("--jira-pass", default=os.environ["JIRA_PASS"], help="JIRA user password")
parser.add_argument("--jira-assignee", default=os.environ["JIRA_ASSIGNEE"], help="JIRA assignee")
parser.add_argument("--jira-storypoints-field", default=os.environ["JIRA_STORYPOINTS_FIELD"], help="JIRA story points")
parser.add_argument("--max-results", default=1000, help="maximum of issues to fetch")
args = parser.parse_args()

if "(" in args.since:
    since = eval(args.since)
else:
    since = dateutil.parser.parse(args.since).date()

requestsParams = {
    'startIndex': '0',
    'jql': 'assignee = %s AND timespent > 0 AND worklogDate >= %s' % (args.jira_assignee, since),
    'fields': 'key,worklog,summary,reporter,link,status,timetracking,%s' % args.jira_storypoints_field,
    'maxResults': args.max_results,
}
response = requests.get(args.jira_url + "rest/api/2/search", requestsParams, auth=(args.jira_user, args.jira_pass))

issues = response.json()['issues']
result = {}
for issue in issues:
    workLogs = issue['fields']['worklog']['worklogs']
    issueKey = issue['key']
    for worklog in workLogs:
        date = dateutil.parser.parse(worklog['started']).date()
        if date < since:
            continue
        dateKey = date.strftime('%Y-%m-%d %a')

        if dateKey not in result:
            result[dateKey] = {
                'total': 0,
                'breakdown': {},
            }
        result[dateKey]['total'] += int(worklog['timeSpentSeconds'])
        storyPoints = issue['fields'].get(args.jira_storypoints_field, 0) or 0
        existingIssue = result[dateKey]['breakdown'].get(issueKey, {})
        worklogTimeSpent = existingIssue.get('worklogTimeSpent', 0)
        result[dateKey]['breakdown'][issueKey] = {
            'title': issue['fields']['summary'],
            'link': '%sbrowse/%s' % (args.jira_url, issueKey),
            'reporter': issue['fields']['reporter']['displayName'],
            'status': issue['fields']['status']['statusCategory']['name'],
            'worklogTimeSpent': worklogTimeSpent + int(worklog['timeSpentSeconds']),
            'originalEstimate': int(issue['fields']['timetracking'].get(
                'originalEstimateSeconds',
                storyPoints * 3600
            )),
            'totalTimeSpent': int(issue['fields']['timetracking']['timeSpentSeconds']),
        }

for key in sorted(result):
    print("%s: %dh" % (key, result[key]['total'] / 3600))
    if args.v:
        for issueKey, issue in result[key]['breakdown'].items():
            print("    %s: %dh" % (issueKey, int(issue['worklogTimeSpent']) / 3600))
    elif args.vv:
        for issueKey, issue in result[key]['breakdown'].items():
            print("  %s:" % issueKey)
            print("    Title: %s" % issue['title'])
            print("    Link: %s" % issue['link'])
            print("    Status: %s" % issue['status'])
            print("    Reporter: %s" % issue['reporter'])
            print("    Worklog timespent: %dh" % (issue['worklogTimeSpent'] / 3600))
            print("    Original estimate: %dh" % (issue['originalEstimate'] / 3600))
            print("    Total timespent: %dh" % (issue['totalTimeSpent'] / 3600))
            if issue['originalEstimate']:
                print("    Estimate accuracy: %5.2f%%" % (issue['totalTimeSpent'] * 100.0 / issue['originalEstimate']))
