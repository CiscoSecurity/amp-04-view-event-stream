try:
    import pika
except:
    print("Python3 Module Pika must be installed for proper operation.")
    print("https://pypi.org/project/pika/")
    exit()
import json
import sys

# Event Stream Username
username = ''

# Event Stream Password
password = ''

# Event Stream Name
queue_name = ''


def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    parsed = json.loads(body)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    print()
    
    '''  
    IMPORTANT!!!!!!!
       If you wish to only use the script to confirm event stream operation; leave this line commented to ensure 
       messages are eventually read into the SEIM queue on resolution of the issue. 
       
       Uncomment the basic_ack line below to remove the message from the AMP event queue on read by the view script. 
       If you do not do this, the message will continue to be sent to the view script on each pull potentially 
       causing memory issues on the machine.
    '''
    # channel.basic_ack(delivery_tag=method_frame.delivery_tag)


# Change the following line to the correct event stream URL if not using the NAM console.
node = pika.URLParameters(f'amqps://{username}:{password}@export-streaming.amp.cisco.com:443')
connection = pika.BlockingConnection(node)
channel = connection.channel()
channel.basic_consume(f'{queue_name}', on_message)
channel.start_consuming()
