#Python2.7.2
'''Example: python jntu_results_bulk.py 08QQ1A04 1036 60 1'''
import sys
import httplib
import string

if len(sys.argv)>4: start = int(sys.argv[4])
else: start = 1
if len(sys.argv)>3: std_max = int(sys.argv[3])
else: std_max = 60
if len(sys.argv)>2: ecode = sys.argv[2]
else: ecode = "1036"
if len(sys.argv)>1: htno = sys.argv[1]
else: htno = "08QQ1A04"

#print htno,ecode,std_max,start

conn = None
resp = None
count = 0

def get_htno(htno, ecode):
    '''Gets the result HTML for the given HTNO and ECODE'''
    global conn, resp, count
    try:
        global conn, resp #for some reason, conn & resp don't exist out of try when not global
        conn = httplib.HTTPConnection("jntu.ac.in")
        conn.request("GET", "/results/htno/"+htno+"/"+ecode+"/index.html")
        resp = conn.getresponse()
    except:
        #print " conn_failed ",
        return get_htno(htno, ecode)
    conn.close()
    if resp.status > 400:
        #print " BAD_STATUS: "+str(resp.status),
        return get_htno(htno, ecode)
    data = resp.read()
    acc = string.find(data, "<center>")
    if acc>-1:  data = data[acc:]
    elif count<10:
        count+=1
        #print " BAD_DATA: "+data,
        return get_htno(htno, ecode)
    else:
        print "Couldn't get a result for "+htno+", with exam-code: "+ecode+", perhaps their database crashed again?"
        count = 0
        return
    count = 0
    print data

for i in xrange(start, std_max+1):
    k = str(i)
    z = 10-(len(htno)+len(k))
    #print k, z
    if z>=0: k = htno+("0"*z)+k
    #print k
    get_htno(k, ecode)