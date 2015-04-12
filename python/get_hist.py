#!/Python27/python
# coding: latin-1
#
print 

import MySQLdb
import json
import collections
from sysconfig import *


def get_hist(linguaggio=sys.argv[1]):
    
    # Apri la connessione al DB
    db = MySQLdb.connect("localhost","jobsearch","000","jobsdb",use_unicode=True)
    # Crea un cursore con il metodo cursor() per eseguire le query
    cursor = db.cursor()
    
    # La query da eseguire
    if linguaggio == "all":
        sql = """SELECT job_lang as lang, count(*) as frequency FROM `joblang` GROUP BY job_lang ORDER BY frequency DESC LIMIT 10"""
    else:
        sql="""SELECT job_lang, count(*) as frequency
                FROM joblang
                JOIN jobposting 
                ON jobposting.job_id = joblang.jobpost_id
                WHERE jobposting.job_language LIKE '%""" + str(linguaggio) + """,%' OR '%, """ +str(linguaggio)+"""%' OR '"""+str(linguaggio)+"""'
                GROUP BY job_lang
                ORDER BY frequency DESC
                LIMIT 10
            """

    #inizializzo la variabile dove aggiungere i dati
    objects_list = []
    
    ## Esecuzione della query. In caso di fallimento, mostra l'errore
    try:
        #Esecuzione della query
        cursor.execute(sql)
        results = cursor.fetchall()
    
        for row in results:
            d = collections.OrderedDict()
            d['language'] = row[0]
            d['frequency'] = int(row[1])
            objects_list.append(d)
    
    except MySQLdb.Error, e:
        sys.stderr.write("[ERROR] %d: %s\n" % (e.args[0], e.args[1]))
    
    #preparo l'header della risposta http ed incollo i dati in formato JSON
    #print 'Content-Type: application/json'
    #print json.dumps(data)
    print json.dumps(objects_list)
    
    # Disconnetti il database
    db.close()

if __name__ == "__main__":
   get_hist(sys.argv[1])