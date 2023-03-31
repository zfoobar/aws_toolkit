import boto3
import json



class sqs_client:

    def __init__(self, queue_url, region):
        self.url = queue_url
        self.client = boto3.client("sqs", region_name=region)
        self.r = None

    def send(self, msg):
        r = self.client.send_message(
            QueueUrl=self.url,
            MessageBody=json.dumps(msg)
            )
        return r

    def recv(self, max_msg=1, wait_time=10):
        r = self.client.receive_message(
                QueueUrl=self.url,
                MaxNumberOfMessages=max_msg,
                WaitTimeSeconds=wait_time,
        )
   
        return len(r.get("Messages", []))

    def unpack_json(self):
        if not self.r:
            return []
        else:
            u = [m['Body'] for m in self.r.get("Messages", []) ]
            return u


if __name__ == "__main__":

    url = "https://sqs.us-east-1.amazonaws.com/160698055680/tq"
    d = {}
    d['dog'] = 'cat'

    c = sqs_client(url,'us-east-1')

    #for i in range(0,100):
    #    print("Sending...")
    #    c.send(d)

    
    r = c.recv(10,1)
    while r:
        for m in c.unpack_json():
            print(m)
        r = c.recv(10,1)
        print(f"DEBUG r: {r}")
