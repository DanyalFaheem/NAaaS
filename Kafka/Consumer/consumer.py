from kafka import KafkaConsumer
from json import loads

# # Receives from producer after every 2 seconds
# consumer.poll(timeout_ms=2000)

class Consumer():
    def __init__(self):
        self.consumer = KafkaConsumer(
            'topic_test1',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group-id',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
    
    def Receive(self):
        for msg in self.consumer:
            print (msg.value)
    
def main():
    cons_obj = Consumer()
    cons_obj.Receive()

if __name__ == "__main__":
    main()