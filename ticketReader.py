import requests
import json
import pytest
import os

print('\n' + "Welcome to the Zendesk ticket viewer!")

userVal = None
response = None
data = None
tickets = None
ticketsPerPage = 25

def get_tickets():

    #url = 'https://zcclandonbrown.zendesk.com/api/v2/tickets.json'
    #user = 'landonnbrownn@gmail.com' + '/token'
    #pwd = '6qS2TPfeafqqgKP6P6EFqndOhpvlD8raTAscRVkl'

    subdomain = input("Please enter your subdomain: ")
    url = 'https://' + subdomain + '.zendesk.com/api/v2/tickets.json'
    user = input('Please enter your email: ')
    pwd = input('Please enter your password: ')

    #url = 'https://zcclandonbrown.zendesk.com/api/v2/tickets.json'
    #user = 'landonnbrownn@gmail.com'
    #pwd = 'P3rryW1nkle'

    global response
    response = requests.get(url, auth=(user, pwd))

    if response.status_code != 200:
        print('Status:', response.status_code, 'ERROR: invalid credentials or API unavailable. Exiting.')
        exit()

    global data
    data = response.json()
    global tickets
    tickets = data['tickets']
    return tickets

def print_details(ticketIndex):
    ticket = tickets[ticketIndex]
    print("Ticket #" + str((ticketIndex + 1)))
    print("Subject: ", ticket['subject'])
    print("Status: ", ticket['status'], '\n')

    print("Assignee ID: ", str(ticket['assignee_id']))
    print("Submitter ID: ", str(ticket['submitter_id']))

    dateVal = ticket['created_at'].find('T')
    timeVal = ticket['created_at'][dateVal + 1:-1]
    dateVal = ticket['created_at'][:dateVal]
    print("Date created: ", dateVal, " at time: ", timeVal, '\n') 

def print_all(pageNum):
    pageIndex = pageNum - 1

    #if there are only 15 tickets but 25 per page

    if ((len(tickets)%ticketsPerPage != 0) and (pageNum > len(tickets)/ticketsPerPage)):
        print('\n' + 'TICKETS ' + str(ticketsPerPage*pageIndex + 1) + " through " + str(ticketsPerPage*pageIndex + len(tickets)%ticketsPerPage) + '\n')
        for i in range(0,len(tickets)%ticketsPerPage): #prints out overflow tickets
            ticketIndex = i + ticketsPerPage*pageIndex
            print_details(ticketIndex)
    
    if ((len(tickets)%ticketsPerPage != 0) and (pageNum <= len(tickets)/ticketsPerPage)):
        print('\n' + 'TICKETS ' + str(ticketsPerPage*pageIndex + 1) + " through " + str(ticketsPerPage*pageIndex + ticketsPerPage) + '\n')
        for i in range(0,ticketsPerPage): #prints out {ticketsPerPage} tickets at a time
            ticketIndex = i + ticketsPerPage*pageIndex
            print_details(ticketIndex)

    if (len(tickets)%ticketsPerPage == 0):
        print('\n' + 'TICKETS ' + str(ticketsPerPage*pageIndex + 1) + " through " + str(ticketsPerPage*pageIndex + ticketsPerPage) + '\n')
        for i in range(0,ticketsPerPage): #prints out {ticketsPerPage} tickets at a time
            ticketIndex = i + ticketsPerPage*pageIndex
            print_details(ticketIndex)

    pageList = ''
    numPages = int(len(tickets) / ticketsPerPage)
    if (len(tickets)%ticketsPerPage != 0):
        numPages = numPages + 1

    for i in range(0, numPages):
        if (i + 1) == (pageNum):
            pageList = pageList + '[' + str(i+1) + ']' + ' '
            continue
        pageList = pageList + str(i+1) + ' '

    print("Page number: ", pageList)

    while True:
        try:
            nextPage = int(input("What page would you like to go to? (enter 0 to return to menu) "))
            if nextPage == 0:
                menu_selection()
                break
            if nextPage > (numPages) or nextPage < 1:
                print ("Invalid input! Try again")
                continue
        except ValueError:
            print("Invalid input! Try again")
            continue
        else:
            break
    
    print_all(nextPage)

def print_one():
    while True:
        try:
            ticketNum = int(input('\n'+ "Enter a ticket number: "))
            if ticketNum > len(tickets) or ticketNum < 1:
                print ("Invalid input! Try again")
                continue
        except ValueError:
            print("Invalid input! Try again")
            continue
        else:
            break

    ticketIndex = ticketNum - 1

    print_details(ticketIndex) 

    menu_selection()

def menu_selection():
    print('\n')
    print("Choose an option to proceed:")
    print("Press 1 to view all tickets")
    print("Press 2 to view a ticket")
    print("Type 'quit' to exit")
    global userVal 
    userVal = input()
    if userVal == 'quit':
        exit()
    if userVal != '1' and userVal != '2':
        print("Invalid input!", '\n')
        menu_selection()
    if (userVal == '1' or userVal == '2') and data == None:
        get_tickets() #only if data has not already been read, connect to the API and load ticket data
    if userVal == '1':
        print_all(1) #print all tickets, starting at page 1
    if userVal == '2':
        print_one()

menu_selection()
