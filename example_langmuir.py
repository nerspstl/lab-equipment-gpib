import pstl_gpib as gpib 
import os

# integer port number (not necessarly gpib address)
PORT = 1
# Files to be saved on computer location
#MYDIR = "C:\\Users\\<youruser>\\Downloads\\"
MYDIR = '~\\Downloads\\'
MYDIR = os.path.expanduser(MYDIR)
# File name
MYFILE = 'TEK.PY'
# Which source i.e. CH1, MATH3, etc.
CHANNEL = 'CH1'

# runit function
def runit(a):
    if a == 0:
        MYFILE = 'TEK0.PY'
        CHANNEL = 'CH1'
    else:
        MYFILE = "TEK%s.PY" % (a)
        CHANNEL = 'CH4'
    tds = gpib.TDS640a(PORT, MYDIR, MYFILE, CHANNEL)
    tds.getwfm()
    return a + 1

## Saves CH1 Source voltage to TEK0.PY
# then askes if you want to continue with 
# langmuir data retrival off CH4 w/ [Y/n]?

cnt = 'Y'
a = 0
a = runit(a)
while cnt == 'Y':
    cnt = input("Continue [Y/n]?>>")
    if cnt == 'Y':
        a = runit(a)
        print('Saved ' + MYFILE + ' in ' + MYDIR)
    elif cnt == 'n':
        print('\nend of program')
    else:
        print('Invalid entry\nenter "n" to exit')



