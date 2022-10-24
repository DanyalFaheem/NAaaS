from ast import main
from time import sleep
from json import dumps
from kafka import KafkaProducer

class Producer():
    def __init__(self):
        # super().__init__()
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
    def SendData(self):
        for j in range(10):
            print("Iteration", j)
            data = {'counter': j}
            self.producer.send('topic_test1', value=data)
            sleep(1)

def main():
    prod_obj = Producer()
    prod_obj.SendData()

if __name__ == "__main__":
    main()