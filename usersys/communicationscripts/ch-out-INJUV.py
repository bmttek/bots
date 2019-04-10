import bots.communication as communication
import bots.botslib as botslib
import posixpath
from bots.botsconfig import *

class ftp(communication.ftp):
    @botslib.log_session
    def outcommunicate(self,*args,**kwargs):
        #get right filename_mask & determine if fixed name (append) or files with unique names
        filename_mask = self.channeldict['filename'] if self.channeldict['filename'] else '*'
        if '{overwrite}' in filename_mask:
            filename_mask = filename_mask.replace('{overwrite}','')
            mode = 'STOR '
        else:
            mode = 'STOR '
        for row in botslib.query('''SELECT idta,filename,numberofresends
                                    FROM ta
                                    WHERE idta>%(rootidta)s
                                      AND status=%(status)s
                                      AND statust=%(statust)s
                                      AND tochannel=%(tochannel)s
                                        ''',
                                    {'tochannel':self.channeldict['idchannel'],'rootidta':self.rootidta,
                                    'status':FILEOUT,'statust':OK}):
            try:
                ta_from = botslib.OldTransaction(row['idta'])
                ta_to = ta_from.copyta(status=EXTERNOUT)
                tofilename = self.filename_formatter(filename_mask,ta_from)
                print("ftp format {}".format(self.channeldict['ftpbinary']))
                if self.channeldict['ftpbinary']:
                    fromfile = botslib.opendata(row['filename'], 'rb','utf-8')
                    self.session.storbinary(mode + tofilename, fromfile)
                else:
                    fromfile = botslib.opendata(row['filename'], 'r','utf-8')
                    self.session.storlines(mode + tofilename, fromfile)
                fromfile.close()
            except:
                txt = botslib.txtexc()
                ta_to.update(statust=ERROR,errortext=txt,filename='ftp:/'+posixpath.join(self.dirpath,tofilename),numberofresends=row['numberofresends']+1)
            else:
                ta_to.update(statust=DONE,filename='ftp:/'+posixpath.join(self.dirpath,tofilename),numberofresends=row['numberofresends']+1)
            finally:
                ta_from.update(statust=DONE)
