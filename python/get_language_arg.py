#!/Python27/python

#
print 

import MySQLdb
import json
import collections
from sysconfig import *


def get_language_arg(linguaggio=sys.argv[1]):
    
    # Apri la connessione al DB
    db = MySQLdb.connect("localhost","jobsearch","000","jobsdb")
    # Crea un cursore con il metodo cursor() per eseguire le query
    cursor = db.cursor()
    
    # La query da eseguire
    if linguaggio == "all":
        sql = """SELECT * FROM jobposting"""
    else:
        sql = """
        SELECT * FROM jobposting WHERE job_language LIKE '%""" + str(linguaggio) + """,%' OR '%, """ +str(linguaggio)+"""%' OR '"""+str(linguaggio)+"""' 
        """
    #print sql
    #inizializzo la variabile dove aggiungere i dati
    data = list()
    objects_list = []
    
    ## Esecuzione della query. In caso di fallimento, mostra l'errore
    try:
        #Esecuzione della query
        cursor.execute(sql)
        results = cursor.fetchall()
    
        # Per ogni riga restituita, scrivi in una lista i valori timekey/freq
        for row in results:
            data.append([int(row[0]), row[1],int(row[2]),row[3],float(row[4]),float(row[5]),row[6],row[7],row[8]])  
    
    
        for row in results:
            d = collections.OrderedDict()
            d['job_id'] = int(row[0])
            d['job_url'] = row[1]
            d['job_counter'] = int(row[2])
            d['job_city'] = row[3]
            d['job_lat'] = float(row[4])
            d['job_long'] = float(row[5])
            d['job_language'] = row[6]
            d['job_degree'] = row[7]
            d['job_skill'] = row[8]
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
   get_language_arg(sys.argv[1])