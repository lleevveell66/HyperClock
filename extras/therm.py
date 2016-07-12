#!/usr/bin/python

# By Brad Goodman
# http://www.bradgoodman.com/
# brad@bradgoodman.com

# Thermostat controller

"""
 Version 1.1 - Fixes Honneywell authentication change in Sept 2014

 run with "-q" to do a quick query
 Run with --help to see all options

 07/11/16 (LEVEL6) Changed AUTH to use the new Total Connect Comfort URL
"""

import urllib2
import urllib
import json
import datetime
import re
import time
import math
import base64
import time
import httplib
import sys
import tty,termios
import getopt
import os
import stat
import subprocess
import string

"""
 Optional - Specify credentials here so you don't need them on command line
 Change these values below
"""

USERNAME="changeme@changeme.ch"
PASSWORD="changeme"
DEVICE_ID=000000
LOGFILENAME="/var/log/therm.log"

# AUTH="https://rs.alarmnet.com/TotalConnectComfort/"
AUTH="https://mytotalconnectcomfort.com/portal/"

tty_fd=None
old_settings=None
stdlog=None

cookiere=re.compile('\s*([^=]+)\s*=\s*([^;]*)\s*')

def client_cookies(cookiestr,container):
  if not container: container={}
  toks=re.split(';|,',cookiestr)
  for t in toks:
    k=None
    v=None
    m=cookiere.search(t)
    if m:
      k=m.group(1)
      v=m.group(2)
      if (k in ['path','Path','HttpOnly']):
        k=None
        v=None
    if k: 
      #print k,v
      container[k]=v
  return container

def export_cookiejar(jar):
  s=""
  for x in jar:
    s+='%s=%s;' % (x,jar[x])
  return s


def status(ex,argv0):
  p=subprocess.Popen(["ps","-e","--format","%p,%c,%a"],stdout=subprocess.PIPE)
  jobs=p.stdout.readlines()
  p.wait()
  for job in jobs:
    job = job.strip()
    args= string.split(job,",")
    params=string.split(args[2]," ")
    if (params.__len__() >= 2):
      if (params[0] == ex) and (params[1] == argv0):
        if (os.getpid() != int(args[0])):
          print "Running on PID",args[0]

def killall(ex,argv0):
  p=subprocess.Popen(["ps","-e","--format","%p,%c,%a"],stdout=subprocess.PIPE)
  jobs=p.stdout.readlines()
  p.wait()
  for job in jobs:
    job = job.strip()
    args= string.split(job,",")
    params=string.split(args[2]," ")
    if (params.__len__() >= 2):
      if (params[0] == ex) and (params[1] == argv0):
        if (os.getpid() != int(args[0])):
          print "Killing PID",args[0]
          subprocess.Popen(['kill',args[0]]).wait()

def log(*strings):
  global stdlog
  string = " ".join(strings)
  st = str(datetime.datetime.now().strftime("%c"))
  st += " "
  st += string
  print st
  st += "\n"
  if not stdlog: return
  try:
    stdlog.write(st)
    stdlog.flush()
  except Exeption as e:
    print "Error writing to stdlog ",e

# Returns character or None on error. Error should WAIT then retry
def init_tty(ttydev):
  global tty_fd
  if tty_fd:
    return
  mode  = os.stat(ttydev).st_mode
  if (not stat.S_ISCHR(mode)):
      raise ttydev,"is not a character device"

  try:
      log ("Opening ",ttydev)
      tty_fd = open(ttydev,"r")
      old_settings=termios.tcgetattr(tty_fd)	
      tty.setraw(tty_fd)
  finally:
       if tty_fd: 
          termios.tcsetattr(tty_fd, termios.TCSADRAIN, old_settings)
  if not tty_fd:
    raise Exception("Couldnt not open tty %s" % ttydev)

def getch(ttydev):
  global tty_fd
  try:
    ch = tty_fd.read(1)
  except Exception as e:
    tty_fd=None
    raise Exception("Could not read from tty %s %s" % (e.message,str(e.args)))
  return ch


def get_login(queryOnly=None,raiseHold=None,dontChange=None,runProgram=None):
    
    cookiejar=None
    print
    print
    print "Run at ",datetime.datetime.now()
    headers={"Content-Type":"application/x-www-form-urlencoded",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"sdch",
            "Host":"mytotalconnectcomfort.com",
            "DNT":"1",
            "Origin":"https://mytotalconnectcomfort.com/portal/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
        }
    conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
    conn.request("GET", "/portal/",None,headers)
    r0 = conn.getresponse()
    #print r0.status, r0.reason
    
    for x in r0.getheaders():
      (n,v) = x
      #print "R0 HEADER",n,v
      if (n.lower() == "set-cookie"): 
        cookiejar=client_cookies(v,cookiejar)
    #cookiejar = r0.getheader("Set-Cookie")
    location = r0.getheader("Location")

    retries=5
    params=urllib.urlencode({"timeOffset":"240",
        "UserName":USERNAME,
        "Password":PASSWORD,
        "RememberMe":"false"})
    #print params
    newcookie=export_cookiejar(cookiejar)
    #print "Cookiejar now",newcookie
    headers={"Content-Type":"application/x-www-form-urlencoded",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"sdch",
            "Host":"mytotalconnectcomfort.com",
            "DNT":"1",
            "Origin":"https://mytotalconnectcomfort.com/portal/",
            "Cookie":newcookie,
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
        }

#    conn = httplib.HTTPSConnection("rs.alarmnet.com")
    conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
#    conn.request("POST", "/TotalConnectComfort/",params,headers)
    conn.request("POST", "/portal/",params,headers)
    r1 = conn.getresponse()
    #print r1.status, r1.reason
    
    for x in r1.getheaders():
      (n,v) = x
      #print "GOT2 HEADER",n,v
      if (n.lower() == "set-cookie"): 
        cookiejar=client_cookies(v,cookiejar)
    cookie=export_cookiejar(cookiejar)
    #print "Cookiejar now",cookie
    location = r1.getheader("Location")
    
    #cookie = r1.getheader("Set-Cookie")
    #print "OrigCookie",cookie
    #print
    # Strip "expires" "httponly" and "path" from cookie
    #newcookie=cookie
    #newcookie=re.sub(";\s*expires=[^;]+","",newcookie)
    #newcookie=re.sub(";\s*path=[^,]+,",";",newcookie)
    #newcookie=re.sub("HttpOnly\s*[^;],","X;",newcookie)
    #newcookie=re.sub(";\s*HttpOnly\s*,",";",newcookie)
    #cookie=newcookie
    


    if ((location == None) or (r1.status != 302)):
        #raise BaseException("Login fail" )
        log("Error: Never got redirect on initial login  status={0} {1}".format(r1.status,r1.reason))
        return


    # Skip second query - just go directly to our device_id, rather than letting it
    # redirect us to it. 

    code=str(DEVICE_ID)

    t = datetime.datetime.now()
    utc_seconds = (time.mktime(t.timetuple()))
    utc_seconds = int(utc_seconds*1000)
    print "Code ",code

    location="/portal/Device/CheckDataSession/"+code+"?_="+str(utc_seconds)
    #print "THIRD"
    headers={
            "Accept":"*/*",
            "DNT":"1",
            #"Accept-Encoding":"gzip,deflate,sdch",
            "Accept-Encoding":"plain",
            "Cache-Control":"max-age=0",
            "Accept-Language":"en-US,en,q=0.8",
            "Connection":"keep-alive",
            "Host":"mytotalconnectcomfort.com",
            "Referer":"https://mytotalconnectcomfot.com/portal/",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36",
            "Cookie":cookie
        }
    conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
#    conn.set_debuglevel(999);
    conn.request("GET", location,None,headers)
    r3 = conn.getresponse()
    if (r3.status != 200):
      log("Error Didn't get 200 status on R3 status={0} {1}".format(r3.status,r3.reason))
      return

    #print r3.status, r3.reason
    rawdata=r3.read()
    j = json.loads(rawdata)
    #print json.dumps(j,sort_keys=True,indent=4, separators=(',', ': '))
    print "Success",j['success']
    print "Live",j['deviceLive']
    print "CurrentTemp",j['latestData']['uiData']["DispTemperature"]
    print "CoolSetpoint",j['latestData']['uiData']["CoolSetpoint"]
    print "HoldUntil",j['latestData']['uiData']["TemporaryHoldUntilTime"]
    print "StatusCool",j['latestData']['uiData']["StatusCool"]
    print "StatusHeat",j['latestData']['uiData']["StatusHeat"]
    
    if (queryOnly != None):
      return

    headers={
            "Accept":'application/json; q=0.01',
            "DNT":"1",
            "Accept-Encoding":"gzip,deflate,sdch",
            'Content-Type':'application/json; charset=UTF-8',
            "Cache-Control":"max-age=0",
            "Accept-Language":"en-US,en,q=0.8",
            "Connection":"keep-alive",
            "Host":"mytotalconnectcomfort.com",
            "Referer":"https://mytotalconnectcomfort.com/portal/",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36",
            'Referer':"/portal/Device/CheckDataSession/"+code,
            "Cookie":cookie
        }

    t = datetime.datetime.now();
    tcode = t.hour * 60 + t.minute;
    holdtime=2
    if (raiseHold): holdtime=6
    t2code = ((t.hour+holdtime)%24) * 60 + t.minute
    t2code = t2code/15
    print "Current time code",tcode,"2-hours",t2code
    cancelHold= {
        "CoolNextPeriod": None,
        "CoolSetpoint": 75,
        "DeviceID": DEVICE_ID,
        "FanMode": None,
        "HeatNextPeriod": None,
        "HeatSetpoint": None,
        "StatusCool": 0,
        "StatusHeat": 0,
        "SystemSwitch": None
        }
    cool2Hold= {
        "CoolNextPeriod": t2code,
        "CoolSetpoint": 74,
        "DeviceID": DEVICE_ID,
        "FanMode": None,
        "HeatNextPeriod": t2code,
        "HeatSetpoint": None,
        "StatusCool": 1,
        "StatusHeat": 1,
        "SystemSwitch": None
        }

    setcool = None
    currentTemp =  j['latestData']['uiData']["DispTemperature"]
    coolSetPoint = j['latestData']['uiData']["CoolSetpoint"] 


    if (runProgram):
        log( "Resume normal program")
    elif (raiseHold):
        log( "Holding at 80 for 6 hours")
        setcool=80
    elif (coolSetPoint < currentTemp):
        log( "Don't do anything - becasue we should already be cooling")
    elif ((currentTemp > 72) and (coolSetPoint > 72)):
        log( "Let's try to get setpoint down to at least 72")
        setcool = 72
    else:
        setcool = int(currentTemp - 2)
        log( "Drop setpoint to %s - becasue we're higher than that" % setcool)
        
    if ((setcool==None) and (not runProgram)):
        return

    if (dontChange):
        log( "Not Changing")
        return
    """
    print 
    print 
    print rawj
    print 
    print 
    print "Location",location
    for (k,v) in headers.iteritems():
        print k,v
    print 
    print 
"""

    if (raiseHold):
        setcool=80

    location="/portal/Device/SubmitControlScreenChanges"
    cool2Hold["CoolSetpoint"] = setcool
    rawj=""
    if (runProgram):
        rawj=json.dumps(cancelHold)
    else:
        rawj=json.dumps(cool2Hold)
    conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
#   conn.set_debuglevel(999);
    conn.request("POST", location,rawj,headers)
    r4 = conn.getresponse()
    if (r4.status != 200): 
      log("Error Didn't get 200 status on R4 status={0} {1}".format(r4.status,r4.reason))
      return
    #print r4.read()

"""
CancelHold
CoolNextPeriod: null
CoolSetpoint: 75
DeviceID: {{DEVICE_ID}}
FanMode: null
HeatNextPeriod: null
HeatSetpoint: null
StatusCool: 0
StatusHeat: 0
SystemSwitch: null

Set explicit cool setpoint
CoolNextPeriod: null
CoolSetpoint: 74
DeviceID: {{DEVICE_ID}}
FanMode: null
HeatNextPeriod: null
HeatSetpoint: null
StatusCool: 1
StatusHeat: 1
SystemSwitch: null

POST
Content-Type:application/json; charset=UTF-8
https://mytotalconnectcomfort.com/portal/Device/SubmitControlScreenChanges

Accept:application/json, text/javascript, */*; q=0.01
Accept-Encoding:gzip,deflate,sdch
Accept-Language:en-US,en;q=0.8
Connection:keep-alive
Content-Length:166
Content-Type:application/json; charset=UTF-8
Cookie:ASP.NET_SessionId=kkotsl4wqcmxktadj0qqrlqv; RememberMe={{USERNAME}}; .ASPXAUTH_TH_A=4E96C23A36F9390F15F7E83E552AB8DB6B3DC00FE62D88D1F3BC7EE19101747AB1F6E22FCEF78A4EE0B785C8402A52AC985B2C5C43EC01D3B90EE22B3DE64DCF8A15D53DDD01795382F0ABFC09451FE6D70B6B1CB9FD8752C3BC3D1171FE8943D6E2C1E6464BD851D0E7136344AB0830B5B05893CD0935A882E648DA06207AC8D4B67E86A74BEA7736651C0F610AC90EB22F3A03D459CCCB7B552668EC346AF7; TrueHomeCheckCookie=; thlang=en-US; __utma=95700044.1206170533.1376491635.1376491635.1376508195.2; __utmb=95700044.6.10.1376508195; __utmc=95700044; __utmz=95700044.1376508195.2.2.utmcsr=wifithermostat.com|utmccn=(referral)|utmcmd=referral|utmcct=/GetConnected/
DNT:1
Host:mytotalconnectcomfort.com
Origin:https://mytotalconnectcomfort.com
Referer:https://mytotalconnectcomfort.com/portal/Device/Control/{{DEVICE_ID}}
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36
X-Requested-With:XMLHttpRequest
Request Payloadview source
{DeviceID:{{DEVICE_ID}}, SystemSwitch:null, HeatSetpoint:null, CoolSetpoint:74, HeatNextPeriod:null,...}
"""

def usage():
    print """
    therm [optons] [ttydev]
    Options:
        -d            Do not really do anyththing
        -r            Raise and hold temperature
        -p            Run normal Program
        -q            Query Only
        -s            Daemon status
        -k            Kill all daemons
        -U username   Use Username
        -P password   Use Password
        -D device_id  Use Device ID
        -l logfile    Log to filename
        
    If no options are given, a ttydef must be specified for interactive
    mode. Interactive mode keys are:
    Q    quit
    q    query
    C    Change Coolpoint
    r    Raise and hold temperature
    p    Run normal program (cancel holds)
    """

dontChange=None
raiseHold=None
runProgram=None
queryOnly=None
logfile=None
args=[]
try:
    opts,args=getopt.getopt(sys.argv[1:],"skl:drpqP:U:D:")
except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)

for o,a in opts:
    if o== '-d':
        dontChange=1
    if o== '-r':
        raiseHold=1
    if o== '-p':
        runProgram=1
    if o== '-q':
        queryOnly=1
    if o== '-P':
        PASSWORD=a
    if o== '-U':
        USERNAME=a
    if o== '-k':
      killall(sys.executable,sys.argv[0])
      sys.exit(0)
    if o== '-s':
      status(sys.executable,sys.argv[0])
      sys.exit(0)
    if o== '-D':
        DEVICE_ID=int(a)
    if o== '-l':
        LOGFILENAME=int(a)

if ((USERNAME == None) or (USERNAME=="") or (PASSWORD == None) or (PASSWORD == "") or (DEVICE_ID ==0)):
  print "User credentials not specified"
  exit(1)


if (LOGFILENAME):
    stdlog=open(LOGFILENAME,"a")

if (raiseHold):
    log ("Non-Interactive raiseHold request")
    get_login(raiseHold=raiseHold)
    exit(0)

if (queryOnly):
    log ("Non-Interactive queryonly request")
    get_login(queryOnly=1)
    exit(0)

if (runProgram):
    log ("Non-Interactive runProgram request")
    get_login(runProgram=runProgram)
    exit(0)


# We need a tty 

if (args.__len__() == 0):
    usage()
    exit(2)

ttydev=args.pop()

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
log("Interactive Mode Started")
while(1):
    try:
      init_tty(ttydev)
      ch = getch(ttydev)
      if (len(ch) == 0):
          pass
      elif (ch == None):
          pass
      elif (ch == chr(3)):
          exit(1)
      elif (ch == 'Q'):
          log("Interactive quit request")
          exit(1)
      elif (ch == 'q'):
          log("Interactive query request")
          d=get_login(queryOnly=1)
      elif (ch == 'p'):
          log("Interactive runProgram request")
          d=get_login(runProgram=1)
      elif (ch == 'r'):
          log("Interactive raiseHold request")
          d=get_login(raiseHold=1)
      elif (ch == 'C'):
          log("Interactive change point request")
          d=get_login(dontChange=dontChange)
      else:
          log("Unknown character ",ch)
    except Exception as e:
      log( "Exception line ",str(sys.exc_traceback.tb_lineno),str(e.args),str(e.args))
      raise(e)
      time.sleep(10)
