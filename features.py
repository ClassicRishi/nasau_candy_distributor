from init import Connection
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

class TimeDelayFeatures:
    def __init__(self,fromdate,todate):
        self.cursor = Connection().get_cursor()
        self.delayfeatures = None
        self.scaler = MinMaxScaler(feature_range=(0,100))
        self.fromdate = fromdate
        self.todate = todate
    def GatherDifference(self):
        cursor = self.cursor
        cursor.execute("SELECT factory,MAX(ABS(DATEDIFF(SHIPDATE,ORDERDATE))) FROM nasau_candy_dataset WHERE ORDERDATE BETWEEN %s AND %s GROUP BY FACTORY",(self.fromdate,self.todate))
        return cursor.fetchall()
    def ExtractFeatures(self):
        raw_data = [i[1] for i in self.GatherDifference()]
        labels = [i[0] for i in self.GatherDifference()]
        return [labels,raw_data]


class ShippingLeadTime():
    def __init__(self):
        self.cursor = Connection().get_cursor()
    def GatherAverage(self,city1,city2,city3,city4,city5):
        cursor = self.cursor
        cursor.execute('''
        SELECT
            city,
            AVG(ABS(DATEDIFF(orderdate, shipdate))) AS mean_shipping_lead_time
        FROM
            nasau_candy_dataset
        WHERE city = %s OR city = %s OR city = %s OR city = %s OR city = %s GROUP BY city''',(city1,city2,city3,city4,city5))
        
        return cursor.fetchall()
    def get_cities(self):
        cursor = self.cursor
        cursor.execute("SELECT city FROM nasau_candy_dataset GROUP BY city")
        return [i[0] for i in cursor.fetchall()]

class RouteVolume():
    def __init__(self):
        self.cursor = Connection().get_cursor()
    def GatherRouteVolume(self,city1,city2,city3,city4,city5):
        cursor = self.cursor
        cursor.execute('''SELECT
            city, COUNT(customer_id)
        FROM
            nasau_candy_dataset
        WHERE city = %s OR city = %s OR city = %s OR city = %s OR city = %s GROUP BY city''',(city1,city2,city3,city4,city5))
        return cursor.fetchall()

class NormalizedLeadTime:
    def __init__(self):
        self.cursor = Connection().get_cursor()
    def GatherNormalizedLeadTime(self,customerid,expected_lead):
        cursor = self.cursor
        cursor.execute("SELECT customer_id, abs(datediff(shipdate,orderdate)), factory FROM nasau_candy_dataset where customer_id = %s",(customerid))
        result = cursor.fetchall()

        normalized_performance = np.array([i[1] for i in result]) / expected_lead

        factories = [i[2] for i in result]
        return pd.DataFrame({
            'factories': factories,
            'Delay in %(Acc. to Expected days)': normalized_performance
        })