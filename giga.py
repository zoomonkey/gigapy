from bs4 import BeautifulSoup as bs
import mechanize
import time
import logging
import random
import string
from random import seed
from random import randint

_n9yo_sleepdelay = 5501  #10001 #3 hours
_other_sleepdelay = randint(360, 10000)

logFile = 'output.log'
logging.basicConfig( filename = logFile,filemode = 'a',level = logging.INFO,format = '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%m/%d/%Y %I:%M:%S %p' )
iscorrect = False
correctindex = 1

def getrandomcallsign():
    return random.choice(string.ascii_letters).upper() + str(random.randint(0, 9)) + \
        random.choice(string.ascii_letters).upper() + random.choice(string.ascii_letters).upper() + \
        random.choice(string.ascii_letters).upper()
def getrandomphone():
    return str(random.randint(1,500)) + "-" + str(random.randint(1,800)) + "-" + str(random.randint(1,9000))

def select_form(form):
    return form.attrs.get('action', None) == '../sweepstakes/process.php'

def select_formX(form):
    return form.attrs.get('action', None) == '../sweepstakes/checkBonus.php'

def findcorrectindex(html):
    global iscorrect
    soup = bs(html, features="html5lib")
    table = soup.find_all("table", {"class": "background"})
    for row in table:
        cells = row.find_all("td")
        text = cells[0].get_text()
        if("Congratulations!" in text):
            iscorrect = True
            logging.info(str(correctindex) + " = RIGHT index!")
            break
        elif("Sorry, that was incorrect!" in text):
            iscorrect = False
            logging.info(str(correctindex) + " = WRONG index")
            break
    return

def hasalreadybeendonetoday(html):
    soup = bs(html, features="html5lib")
    table = soup.find_all("table", {"class": "background"})
    for row in table:
        cells = row.find_all("td")
        text = cells[0].get_text()
        if("Your callsign has already answered" in text):
            logging.info("Oops!  Already entered for today")
            return True
        else:
            logging.info("Question has NOT been answered today.")
        return False
    return

def main(call, email, phone):
    global correctindex
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('http://www.gigaparts.com/sweepstakes')
    br.select_form(predicate=select_form)

    ctl =  br.form.find_control('callsign')
    logging.info(call)
    ctl.value = call

    ctl1 = br.form.find_control('email')
    logging.info(email)
    ctl1.value = email

    ctl2 = br.form.find_control('phone')
    ctl2.value = phone

    logging.info(phone)
    response = br.submit()

    #NEXT PAGE *******************
    #guess
    logging.info('try guess')
    if(not hasalreadybeendonetoday(response)):
        br.select_form(predicate=select_formX)
        br.form.set_value([str(correctindex)],name='choice')
        response = br.submit()
        findcorrectindex(response)
    elif(not iscorrect):
        findcorrectindex(response)
    return

if(__name__== "__main__"):
    try:
        logging.info("start ---------------------------------------------")
        hasRonBeenRun = False

        correctindex = 1
        for i in range(0, 4):  #loop only max 3 times!  if the index is at 4 no need to run it again
            logging.info('current index=' + str(correctindex))
            if(not iscorrect and correctindex != 4):
                time.sleep(_other_sleepdelay)
                call = getrandomcallsign()
                email = call + "@qrz.com"
                phone = getrandomphone()

                logging.info("run " + call)
                main(call, email, phone)
            else:
                time.sleep(_n9yo_sleepdelay)
                logging.info("run N9YO")
                main("N9YO", "zoomonkey@gmail.com", "636-542-8220")
                break
            if(not iscorrect):
                correctindex += 1
        logging.info("end  ---------------------------------------------")
    except:
        logging.info("error occurred")
