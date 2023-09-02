from influxdb_client import Point
class Pulse:
    label = str(__name__).lower()
    def __init__(self,data):
        measurement = data['liveMeasurement']
        timestamp = measurement['timestamp']
        power = measurement['power']
        cost = measurement.get('accumulatedCost',None)
        lastMeterConsumption = measurement['lastMeterConsumption']
        tags = {self.label: ""}
        fields = {
            "power": float(power),
            "lastMeterConsumption": float(lastMeterConsumption)
        }
        if cost is not None:
            fields.update({'accumulatedCost':cost})
        self.datapoint = {"fields": fields,
                     "tags": tags,
                     "measurement": "pulse",
                     "time": timestamp
                     }
    def get_datapoint(self):
        return Point(measurement_name=str(self.label)).from_dict(self.datapoint)

