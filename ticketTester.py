import requests
import json
import pytest
import os

def get_tickets(subdomain, user, pwd):

    url = 'https://' + subdomain + '.zendesk.com/api/v2/tickets.json'

    global response
    response = requests.get(url, auth=(user, pwd))

    if response.status_code != 200:
        print('Status:', response.status_code, 'Error connecting to the API. Exiting.')
        return 'ERROR: Invalid credentials or API unavailable'
    else:
        global data
        data = response.json()
        global tickets
        tickets = data['tickets']
        if tickets != None:
            return True
        else:
            return False

def print_details(ticketIndex):
    ticket = tickets[ticketIndex]
    return ticket['subject']
    print("Ticket #" + str((ticketIndex + 1)))
    print("Subject: ", ticket['subject'])
    print("Status: ", ticket['status'], '\n')

    print("Assignee ID: ", str(ticket['assignee_id']))
    print("Submitter ID: ", str(ticket['submitter_id']))

    dateVal = ticket['created_at'].find('T')
    timeVal = ticket['created_at'][dateVal + 1:-1]
    dateVal = ticket['created_at'][:dateVal]
    print("Date created: ", dateVal, " at time: ", timeVal, '\n') 

def print_all(pageNum, numTickets, ticketsPerPage):
    numPages = int(len(tickets) / ticketsPerPage) 
    if (len(tickets)%ticketsPerPage != 0):
        numPages = numPages + 1

    if pageNum > numPages:
        return False

    pageList = ''

    for i in range(0, numPages):
        if (i + 1) == (pageNum):
            pageList = pageList + '[' + str(i+1) + ']' + ' '
            continue
        pageList = pageList + str(i+1) + ' '
    
    return pageList

def print_one(ticketNum):
    if not isinstance(ticketNum, int):
        return "Invalid input (must be an integer)! Try again"
    if ticketNum > len(tickets) or ticketNum < 1:
        return "Index out of range! Try again"
    else:
        return True

def test_API():
    assert get_tickets('this', 'wont', 'work') == 'ERROR: Invalid credentials or API unavailable' #if the credentials are invalid, output an appropriate error

    #storing personal information in environmental variables
    subdomain = os.environ.get('ZCC_SUBDOMAIN')
    user = os.environ.get('ZCC_USER')
    pwd = os.environ.get('ZCC_PWD')
    assert get_tickets(subdomain, user, pwd) == True #if credentials ARE valid, function should return true

def test_printing():
    assert print_details(0) == tickets[0]['subject'] #making sure the print function accesses the ticket correctly
    assert print_details(1) != tickets[0]['subject'] #if these two values are different, then the print function did not work properly

def test_paging():
    assert print_all(5, 100, 25) == False #if the page number provided is greater than the # of tickets + overflow, then paging will not work (and should return false)
    assert print_all(1, 100, 25) == '[1] 2 3 4 ' #should return the correct number of pages and in turn, a string of the page indices
    assert print_all(1, 100, 15) == '[1] 2 3 4 5 6 7 '

def test_getOne():
    assert print_one(101) == "Index out of range! Try again" #if a ticket index is out of the range of tickets.json, give an error message
    assert print_one(17) == True #if ticket is within range, function should return true
    assert print_one('abc') == "Invalid input (must be an integer)! Try again" #if invalid input is given, different error message should be outputted
