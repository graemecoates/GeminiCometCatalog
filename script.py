import ephem, os, shutil, ftplib, urllib.request
from datetime import date, datetime

def downloadFile(url,file_name):
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

cometURL = 'https://minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt'
cometLocalFile = 'Soft03Cmt.txt'
cometOutputFile = 'comets.guc'
gatech = ephem.Observer()
gatech.lat, gatech.lon = 51.4769, 0.0005
gatech.date = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')
geminiIPAddr = '192.168.10.52'
geminiFTPPort = 21
geminiUsername = 'admin'
geminiPassword = ''

if os.path.exists(cometOutputFile):
    print('Removing old '+str(cometOutputFile))
    os.remove(cometOutputFile)
if os.path.exists(cometLocalFile):
    print('Removing old '+str(cometLocalFile))
    os.remove(cometLocalFile)
downloadFile(cometURL, cometLocalFile)

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
