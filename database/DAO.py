from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gr.Country as nazione
from go_retailers gr
order by  gr.Country """

        cursor.execute(query)

        for row in cursor:
            result.append(row["nazione"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
from go_retailers gr 
where gr.Country =%s """

        cursor.execute(query,(nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getConnessioni(nazione,anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  t1.r1 as v1,t2.r2 as v2, count(distinct t1.p1) as peso
from (select gr.Retailer_code as r1, gds.Product_number as p1
from go_retailers gr, go_daily_sales gds 
where gr.Country =%s and gds.Retailer_code =gr.Retailer_code and 
YEAR(gds.`Date`)=%s) as t1,
(select gr.Retailer_code as r2 , gds.Product_number  as p2
from go_retailers gr, go_daily_sales gds 
where gr.Country =%s and gds.Retailer_code =gr.Retailer_code and YEAR(gds.`Date`)=%s) as t2
where t1.p1=t2.p2 and t1.r1<t2.r2
group by  t1.r1,t2.r2"""

        cursor.execute(query,(nazione,anno,nazione,anno,))

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result
