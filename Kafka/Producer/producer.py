# from ast import main
from time import sleep
from json import dumps
from json import load
from kafka import KafkaProducer

class Producer():
    def __init__(self):
        # super().__init__()
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
    def SendData(self):
        with open('jsons/2021/2021-11-20/Scrapped.json') as json_file:
            data = load(json_file)
            self.producer.send('topic_test1', value=data)
            sleep(1)
            # print(type(data))
            # print(data)
            # print(data["Header"])

        for j in range(10):
            print("Iteration", j)
            data = {'counter': j}
            

def main():
    prod_obj = Producer()
    prod_obj.SendData()

if __name__ == "__main__":
    main()