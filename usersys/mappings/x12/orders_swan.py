#mapping-script
from x12lib import get_art_num          #import x12 specifc helper function
import bots.transform as transform      #import div bots helper functions
import mysql.connector
import os, sys
import bots.botsglobal as botsglobal
from datetime import datetime
import isbn as fnisbn

dbConfig = {
  'host':"********",
  'user':"bibRobot",
  'password':"*******",
  'database':"********"
}
updateOrder = ("UPDATE orderRecords SET author=%s, poNumber=%s, swanRecordNumber=%s, lineNumber=%s, ordered_at=%s WHERE id=%s")
insertLog = ("INSERT INTO OLPL_Apps_Bib_Log (funcName, transType, recordIdent, Message, dateCreated) VALUES (%s, %s, %s, %s, %s)")

def main(inn,out):
    #setup variables
    orderNumber="none"
    lineNumber="0"
    isbn="none"
    title="none"
    author="none"
    price="0.00"
    qty="0"
    fund="none"
    holdingCode="none"
    swanRecordNumber="none"
    holdingCodeDB="none"
    recordId=0
    #get global fields
    orderNumber=inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG03':None})
    #start x12 document
    out.put({'BOTSID':'ST','ST01':'850','ST02':inn.get({'BOTSID':'ST','ST02':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG01':'00'})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG02':'NE'})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG03':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG03':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG04':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG04':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG05':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG05':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG06':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG06':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG07':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG07':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG08':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG08':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG09':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG09':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG10':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG10':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BEG','BEG11':inn.get({'BOTSID':'ST'},{'BOTSID':'BEG','BEG11':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF01':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF01':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF02':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF02':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF03':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF03':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF04':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF04':None})})
    for party in inn.getloop({'BOTSID':'ST'},{'BOTSID':'N1'}):
        pou = out.putloop({'BOTSID':'ST'},{'BOTSID':'N1'})
        pou.put({'BOTSID':'N1','N101':party.get({'BOTSID':'N1','N101':None})})
        pou.put({'BOTSID':'N1','N102':party.get({'BOTSID':'N1','N102':None})})
        pou.put({'BOTSID':'N1','N103':party.get({'BOTSID':'N1','N103':None})})
        pou.put({'BOTSID':'N1','N104':party.get({'BOTSID':'N1','N104':None})})
        pou.put({'BOTSID':'N1','N105':party.get({'BOTSID':'N1','N105':None})})
        pou.put({'BOTSID':'N1','N106':party.get({'BOTSID':'N1','N106':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N2','N201':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N2','N201':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N2','N202':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N2','N202':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N3','N301':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N3','N301':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N3','N302':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N3','N302':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N4','N401':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N4','N401':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N4','N402':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N4','N402':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N4','N403':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N4','N403':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N4','N404':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N4','N404':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N4','N405':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N4','N405':None})})
        pou.put({'BOTSID':'N1'},{'BOTSID':'N4','N406':party.get({'BOTSID':'N1','N101':'ST',},{'BOTSID':'N4','N406':None})})
    #LINES***************************************
    for lin in inn.getloop({'BOTSID':'ST'},{'BOTSID':'PO1'}):
        #get line variables
        lineNumber=lin.get({'BOTSID':'PO1','PO101':None})
        recordId=0
        holdingCodeDB="none"
        qty=lin.get({'BOTSID':'PO1','PO102':None})
        price=lin.get({'BOTSID':'PO1','PO104':None})
        isbn=lin.get({'BOTSID':'PO1','PO107':None})
        swanRecordNumber=lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN10':None})
        holdingCode=lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN14':None})
        for pid in lin.getloop({'BOTSID':'PO1'},{'BOTSID':'PID'}):
            if pid.get({'BOTSID':'PID','PID04':None}) == "A1":
                author=pid.get({'BOTSID':'PID','PID05':None})
            if pid.get({'BOTSID':'PID','PID04':None}) == "T1":
                if pid.get({'BOTSID':'PID','PID06':None}) is not None:
                    if len(pid.get({'BOTSID':'PID','PID06':None})) > 2:
                        title="{}{}{}".format(pid.get({'BOTSID':'PID','PID05':None}),pid.get({'BOTSID':'PID','PID06':None}),pid.get({'BOTSID':'PID','PID07':None}))
                    else:
                        title=pid.get({'BOTSID':'PID','PID05':None})
                else:
                     title=pid.get({'BOTSID':'PID','PID05':None})
        title=title.replace("*"," ")
        #get record from sql and check holding code -- update record
        #setup database logging
        cnx=None
        cnxLog=None
        cursorLog=None
        cursor=None
        recordID=None
        addPO="no"
        try:
           cnxLog = mysql.connector.connect(**dbConfig)
           cursorLog = cnxLog.cursor()
        except Exception as eLog:
            botsglobal.logger.info("---Error with log database connection {}".format(eLog))
        now = datetime.now()
        dt = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            cnx = mysql.connector.connect(**dbConfig)
            cursor = cnx.cursor()
            if "." not in price:
                price = "{}.00".format(price)
            isbn_other = ""
            if fnisbn.isbn_type(isbn) == 'ISBN10':
                isbn_other = fnisbn.to_isbn13(isbn)
            else:
                isbn_other = fnisbn.to_isbn10(isbn)
            #cursor.execute("SELECT * FROM orderRecords WHERE isbn=%s AND price=%s AND qty=%s AND ordered_at < '1902-01-01'", (isbn,price,qty))
            cursor.execute("SELECT * FROM orderRecords WHERE (isbn=%s OR isbn=%s) AND (price=%s AND qty=%s AND ack_at < '1902-01-01')", (isbn,isbn_other,price,qty))
            result = cursor.fetchall()
            if result is not None:
                if len(result) == 1:
                    for record in result:
                        recordID=record[0]
                        holdingCodeDB=record[6]
                        if holdingCode != holdingCodeDB:
                            holdingCode = holdingCodeDB
                        values=(author,orderNumber,swanRecordNumber,lineNumber,dt,recordID)
                        cursor.execute(updateOrder,values)
                        valuesLog=("updateOrderRecord","Order",orderNumber,"order record updated",dt)
                        cursorLog.execute(insertLog,valuesLog)
                        cnx.commit()
                        cnxLog.commit()
                        cursor.close()
                        cursorLog.close()
                        cnx.close()
                        cnxLog.close()
                        addPO="yes"
                else:
                    if(len(result)) == 0:
                        botsglobal.logger.info("No order records returned")
                        valuesLog=("updateOrderRecord","Order",orderNumber,"no order records returned",dt)
                        cursorLog.execute(insertLog,valuesLog)
                        cnxLog.commit()
                        cursorLog.close()
                        cnxLog.close()
                        addPO="no"
                    else:
                        botsglobal.logger.info("More then 1 order record returned")
                        valuesLog=("updateOrderRecord","Order",orderNumber,"more then one order records returned",dt)
                        cursorLog.execute(insertLog,valuesLog)
                        cnxLog.commit()
                        cursorLog.close()
                        cnxLog.close()
                        addPO="no"
        except Exception as e:
            botsglobal.logger.info("---Error with database connection {} with trace {}".format(e,sys.exc_info()))
            valuesLog=("updateOrderRecord","Order",orderNumber,"Error with database connection {} with trace {}".format(e,sys.exc_info()),dt)
            cursorLog.execute(insertLog,valuesLog)
            cnxLog.commit()
            cursorLog.close()
            cnxLog.close()
        if addPO == "yes":
            lou = out.putloop({'BOTSID':'ST'},{'BOTSID':'PO1'})
            lou.put({'BOTSID':'PO1','PO101':lin.get({'BOTSID':'PO1','PO101':None})})
            lou.put({'BOTSID':'PO1','PO102':lin.get({'BOTSID':'PO1','PO102':None})})
            lou.put({'BOTSID':'PO1','PO103':lin.get({'BOTSID':'PO1','PO103':None})})
            lou.put({'BOTSID':'PO1','PO104':lin.get({'BOTSID':'PO1','PO104':None})})
            lou.put({'BOTSID':'PO1','PO105':lin.get({'BOTSID':'PO1','PO105':None})})
            lou.put({'BOTSID':'PO1','PO106':lin.get({'BOTSID':'PO1','PO106':None})})
            lou.put({'BOTSID':'PO1','PO107':lin.get({'BOTSID':'PO1','PO107':None})})
            lou.put({'BOTSID':'PO1','PO108':lin.get({'BOTSID':'PO1','PO108':None})})
            lou.put({'BOTSID':'PO1','PO109':lin.get({'BOTSID':'PO1','PO109':None})})
            lou.put({'BOTSID':'PO1','PO110':lin.get({'BOTSID':'PO1','PO110':None})})
            lou.put({'BOTSID':'PO1','PO111':lin.get({'BOTSID':'PO1','PO111':None})})
            lou.put({'BOTSID':'PO1','PO112':lin.get({'BOTSID':'PO1','PO112':None})})
            lou.put({'BOTSID':'PO1','PO113':lin.get({'BOTSID':'PO1','PO113':None})})
            for pid in lin.getloop({'BOTSID':'PO1'},{'BOTSID':'PID'}):
                pou = lou.putloop({'BOTSID':'PO1'},{'BOTSID':'PID'})
                pou.put({'BOTSID':'PID','PID01':pid.get({'BOTSID':'PID','PID01':None})})
                pou.put({'BOTSID':'PID','PID02':pid.get({'BOTSID':'PID','PID02':None})})
                pou.put({'BOTSID':'PID','PID03':pid.get({'BOTSID':'PID','PID03':None})})
                pou.put({'BOTSID':'PID','PID04':pid.get({'BOTSID':'PID','PID04':None})})
                usePID6="true"
                usePID7="true"
                if pid.get({'BOTSID':'PID','PID06':None}) is not None:
                    if len(pid.get({'BOTSID':'PID','PID06':None})) > 2:
                        title="{}{}{}".format(pid.get({'BOTSID':'PID','PID05':None}),pid.get({'BOTSID':'PID','PID06':None}),pid.get({'BOTSID':'PID','PID07':None}))
                        usePID6="false"
                        usePID7="false"
                    else:
                        title=pid.get({'BOTSID':'PID','PID05':None})
                else:
                    title=pid.get({'BOTSID':'PID','PID05':None})
                title=title.replace("*"," ")
                pou.put({'BOTSID':'PID','PID05':title})
                if usePID6 == "true":
                    pou.put({'BOTSID':'PID','PID06':pid.get({'BOTSID':'PID','PID06':None})})
                if usePID7 == "true":
                    pou.put({'BOTSID':'PID','PID07':pid.get({'BOTSID':'PID','PID07':None})})
                pou.put({'BOTSID':'PID','PID08':pid.get({'BOTSID':'PID','PID08':None})})
                pou.put({'BOTSID':'PID','PID09':pid.get({'BOTSID':'PID','PID09':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF01':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF01':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF02':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF02':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF03':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF03':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF04':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF04':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'MSG','MSG01':lin.get({'BOTSID':'PO1'},{'BOTSID':'MSG','MSG01':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'MSG','MSG02':lin.get({'BOTSID':'PO1'},{'BOTSID':'MSG','MSG02':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN01':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN01':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN02':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN02':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN03':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN03':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN04':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN04':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN05.01':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN05.01':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN06':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN06':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN07':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN07':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN08':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN08':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN09':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN09':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN10':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN10':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN11':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN11':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN12':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN12':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN13':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN13':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN14':holdingCode})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN15':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN15':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN16':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN16':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN17':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN17':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN18':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN18':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN19':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN19':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN20':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN20':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN21':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN21':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN22':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN22':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN23':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN23':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN24':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN24':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN25':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN25':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN26':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN26':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN27':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN27':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN28':lin.get({'BOTSID':'PO1'},{'BOTSID':'SLN','SLN28':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT01':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT01':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT02':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT02':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT03':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT03':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT04':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT04':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT05':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT05':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT06':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT06':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT07':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT07':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'SE','SE01':inn.get({'BOTSID':'ST'},{'BOTSID':'SE','SE01':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'SE','SE02':inn.get({'BOTSID':'ST'},{'BOTSID':'SE','SE02':None})})
