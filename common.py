import datetime
# cache system time prior to running code block
def start(message):
    global TIMER
    print "\n" + message
    TIMER = datetime.datetime.now()


# output current time - start time with debug msg
def end(message):
    global TIMER
    end = datetime.datetime.now()
    print "\n" + message + " in %s seconds.\n" % str((end-TIMER).seconds)
    TIMER = None