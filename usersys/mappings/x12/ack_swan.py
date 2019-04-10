#mapping-script
from x12lib import get_art_num          #import x12 specifc helper function
import bots.transform as transform      #import div bots helper functions
import mysql.connector
import os, sys
import bots.botsglobal as botsglobal
from datetime import datetime
import isbn as fnisbn

dbConfig = {
  'host':"192.168.54.205",
  'user':"bibRobot",
  'password':"Olpl114477?",
  'database':"OLPL_Apps_BibRobot"
}
updateOrder = ("UPDATE orderRecords SET ack_at=%s, ack_result=%s WHERE id=%s")
insertLog = ("INSERT INTO OLPL_Apps_Bib_Log (funcName, transType, recordIdent, Message, dateCreated) VALUES (%s, %s, %s, %s, %s)")

def main(inn,out):
    #setup variables
    orderNumber="none"
    lineNumber="0"
    isbn="none"
    price="0.00"
    qty="0"
    recordId=0
    now = datetime.now()
    dt = now.strftime('%y%m%d')
    #get global fields
    #start x12 document

    out.put({'BOTSID':'ST','ST01':'855','ST02':inn.get({'BOTSID':'ST','ST02':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK01':inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK01':None})})
    #out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK02':'AT'})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK03':inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK03':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK04':dt})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK05':inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK05':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK06':inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK06':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK07':inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK07':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK08':inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK08':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'BAK','BAK09':inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK09':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF01':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF01':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF02':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF02':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF03':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF03':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'REF','REF04':inn.get({'BOTSID':'ST'},{'BOTSID':'REF','REF04':None})})
    orderNumber=inn.get({'BOTSID':'ST'},{'BOTSID':'BAK','BAK03':None})
    #LINES***************************************
    for lin in inn.getloop({'BOTSID':'ST'},{'BOTSID':'PO1'}):
        #get line variables
        lineNumber=lin.get({'BOTSID':'PO1','PO101':None})
        #recordId=0
        #holdingCodeDB="none"
        qty=lin.get({'BOTSID':'PO1','PO102':None})
        ackResult=lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK01':None})
        price=lin.get({'BOTSID':'PO1','PO104':None})
        isbn=lin.get({'BOTSID':'PO1','PO107':None})
        for pid in lin.getloop({'BOTSID':'PO1'},{'BOTSID':'PID'}):
            if pid.get({'BOTSID':'PID','PID04':None}) == "A1":
                author=pid.get({'BOTSID':'PID','PID05':None})
            if pid.get({'BOTSID':'PID','PID04':None}) == "T1":
                title=pid.get({'BOTSID':'PID','PID05':None})
        #get record from sql and check holding code -- update record
        #setup database logging
        cnx=None
        cnxLog=None
        cursorLog=None
        cursor=None
        recordID=None
        addPO="yes"
        try:
           cnxLog = mysql.connector.connect(**dbConfig)
           cursorLog = cnxLog.cursor()
        except Exception as eLog:
            botsglobal.logger.info("---Error with log database connection {}".format(eLog))
        now = datetime.now()
        dtLong = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            cnx = mysql.connector.connect(**dbConfig)
            cursor = cnx.cursor()
            price = "{:.2f}".format(float(price))
            isbn_other = ""
            if fnisbn.isbn_type(isbn) == 'ISBN10':
                isbn_other = fnisbn.to_isbn13(isbn)
            else:
                isbn_other = fnisbn.to_isbn10(isbn)
            cursor.execute("SELECT * FROM orderRecords WHERE (isbn=%s OR isbn=%s) AND (price=%s AND qty=%s AND ack_at < '1902-01-01' AND poNumber=%s)", (isbn,isbn_other,price,qty,orderNumber))
            result = cursor.fetchall()
            if result is not None:
                if len(result) == 1:
                    for record in result:
                        recordID=record[0]
                        values=(dtLong,ackResult,recordID)
                        cursor.execute(updateOrder,values)
                        valuesLog=("updateOrderRecord","Order","Order-{} isbn-{}".format(orderNumber,isbn),"order record updated",dt)
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
                        valuesLog=("updateOrderRecord","Order","Order-{} isbn-{}".format(orderNumber,isbn),"no order records returned",dt)
                        cursorLog.execute(insertLog,valuesLog)
                        cnxLog.commit()
                        cursorLog.close()
                        cnxLog.close()
                        addPO="no"
                    else:
                        botsglobal.logger.info("More then 1 order record returned")
                        valuesLog=("updateOrderRecord","Order","Order-{} isbn-{}".format(orderNumber,isbn),"more then one order records returned",dt)
                        cursorLog.execute(insertLog,valuesLog)
                        cnxLog.commit()
                        cursorLog.close()
                        cnxLog.close()
                        addPO="no"
        except Exception as e:
            print("logOrderNumber={}".format(orderNumber))
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
                pou.put({'BOTSID':'PID','PID05':pid.get({'BOTSID':'PID','PID05':None})})
                pou.put({'BOTSID':'PID','PID06':pid.get({'BOTSID':'PID','PID06':None})})
                pou.put({'BOTSID':'PID','PID07':pid.get({'BOTSID':'PID','PID07':None})})
                pou.put({'BOTSID':'PID','PID08':pid.get({'BOTSID':'PID','PID08':None})})
                pou.put({'BOTSID':'PID','PID09':pid.get({'BOTSID':'PID','PID09':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF01':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF01':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF02':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF02':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF03':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF03':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'REF','REF04':lin.get({'BOTSID':'PO1'},{'BOTSID':'REF','REF04':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK01':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK01':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK02':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK02':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK03':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK03':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK04':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK04':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK05':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK05':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK06':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK06':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK07':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK07':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK08':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK08':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK09':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK09':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK10':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK10':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK11':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK11':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK12':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK12':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK13':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK13':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK14':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK14':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK15':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK15':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK16':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK16':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK17':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK17':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK18':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK18':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK19':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK19':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK20':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK20':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK21':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK21':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK22':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK22':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK23':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK23':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK24':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK24':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK25':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK25':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK26':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK26':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK27':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK27':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK28':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK28':None})})
            lou.put({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK29':lin.get({'BOTSID':'PO1'},{'BOTSID':'ACK','ACK29':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT01':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT01':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT02':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT02':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT03':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT03':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT04':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT04':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT05':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT05':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT06':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT06':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'CTT','CTT07':inn.get({'BOTSID':'ST'},{'BOTSID':'CTT','CTT07':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'SE','SE01':inn.get({'BOTSID':'ST'},{'BOTSID':'SE','SE01':None})})
    out.put({'BOTSID':'ST'},{'BOTSID':'SE','SE02':inn.get({'BOTSID':'ST'},{'BOTSID':'SE','SE02':None})})

