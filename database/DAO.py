from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO:

    @staticmethod
    def DAOgetStores():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select s.*
                    from stores s """
        cursor.execute(query)

        results = []
        for row in cursor:
            results.append(Store(**row))

        cnx.close()
        cursor.close()

        return results

    @staticmethod
    def DAOgetNodes(id):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select o.*
                    from orders o
                    where o.store_id = %s"""
        cursor.execute(query, (id, ))

        results = []
        for row in cursor:
            results.append(Order(**row))

        cnx.close()
        cursor.close()

        return results

    @staticmethod
    def DAOgetArchi(store_id, giorni):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select o1.order_id as u, o2.order_id as v, SUM(oi1.quantity) + SUM(oi2.quantity) as peso 
                    from orders o1, orders o2, order_items oi1, order_items oi2
                    where o1.store_id = o2.store_id and o1.store_id = %s and o2.order_date < o1.order_date
                    and DATEDIFF(o1.order_date, o2.order_date) < %s and oi1.order_id = o1.order_id and oi2.order_id = o2.order_id 
                    group by o1.order_id, o2.order_id """
        cursor.execute(query, (store_id, giorni))

        results = []
        for row in cursor:
            results.append((row["u"], row["v"], row["peso"]))

        cnx.close()
        cursor.close()

        return results
