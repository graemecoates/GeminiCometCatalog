import ephem, os, shutil, ftplib, urllib.request
from datetime import date, datetime

def downloadFile(url,file_name):
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

        
## Parameters
        
cometURL = 'https://minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt'
cometLocalFile = 'Soft03Cmt.txt'
cometOutputFile = 'comets.guc'
geminiIPAddr = '192.168.10.52'              # Change this to point at your Gemini 2 Mount
geminiFTPPort = 21              # Unlikely this needs to change unless you're doing some odd NAT type stuff...
geminiUsername = 'admin'            # default = 'admin'
geminiPassword = ''             # default = ''

## Setup Observer details

gatech = ephem.Observer()
gatech.lat, gatech.lon = 51.4769, 0.0005            # Change this to match your observing location
gatech.date = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')



## Shift out any old files

if os.path.exists(cometOutputFile):
    print('Removing old '+str(cometOutputFile))
    os.remove(cometOutputFile)
if os.path.exists(cometLocalFile):
    print('Removing old '+str(cometLocalFile))
    os.remove(cometLocalFile)
downloadFile(cometURL, cometLocalFile)

## Calculate geocentric positions for now using elements

with open(cometOutputFile,"a") as o:
    print('Calculate positions from elements')
    with open(cometLocalFile) as f:
        elementList=f.readlines()
        for element in elementList:
            if element[0]=='#':
                # print(element)
                continue
            yh=ephem.readdb(element)
            yh.compute(gatech)
            o.write(str(yh.name)+','+str(yh.ra)+','+str(yh.dec)+','+str(yh.name)+'\n')
            #print('%s %s %s' % (yh.name, yh.ra, yh.dec))
f.close()
o.close()


## Upload via ftp 

print("Open FTP")
ftpSession = ftplib.FTP()
ftpSession.connect(geminiIPAddr,geminiFTPPort)
ftpSession.login(geminiUsername,geminiPassword)
ftpSession.cwd('Catalogs')
#ftpSession.retrlines('LIST')
with open(cometOutputFile,'rb') as f:                           # file to send
    try:
        ftpSession.delete(cometOutputFile)
        print('Old '+ str(cometOutputFile) + ' deleted')
    except:
        print(str(cometOutputFile) + ' not present to delete')
    print('STOR file')
    ftpSession.storbinary('STOR '+str(cometOutputFile), f)     # send the file
print('Close FTP')
f.close()                                    # close file and FTP
ftpSession.quit()
print('Comet upload done')
