#!/usr/bin/python
import re
import time
import json
import psutil
import os
import boto.ec2
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

bot_id = os.environ.get("BOT_ID")

# Start connection
if slack_client.rtm_connect():
    print("Jasper connected and running")

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % bot_id):

                print("Message received: %s" % json.dumps(message, indent=2))

                message_text = message['text']. \
                    split("<@%s>" % bot_id)[1]. \
                    strip()

                conn = boto.ec2.connect_to_region("us-west-2", aws_access_key_id=<aws_access_key_id>,
                                                  aws_secret_access_key=<aws_secret_access_key>)

                # Jasper Help
                help = 'Try these ' + '\n' + '*create <ami_id> <instance_type> <key_pair> <link>*' + '\n'
                if re.match(r'.*(help).*', message_text, re.IGNORECASE):
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text=help,
                        as_user=True)

                # Create EC2 Instance
                if re.match(r'.*(create).*', message_text, re.IGNORECASE):
                    key_pair = message_text.split()[3]
                    with open(key_pair, 'w') as keyfile:
                        key_aws = conn.create_key_pair(key_pair)
                        key_aws.save('.')

                    time.sleep(5)

                    ami_id = message_text.split()[1]
                    instance_id = message_text.split()[2]
                    reservation = conn.run_instances(ami_id, instance_type=instance_id, key_name=key_pair)

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Creating server with AMI {}".format(ami_id),
                        as_user=True)

                    instance = reservation.instances[0]

                    attachment = message_text.split()[4]
                    attachment = re.sub('[<>]', '', attachment)
                    while instance.state != 'running':
                        global instance_ip
                        instance.update()
                        instance_ip = instance.ip_address
                        os.system("ssh -i %s -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -q ubuntu@%s 'cd ~; wget %s'" %(key_pair + '.pem', instance_ip, attachment))

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Server created with IP {} and {} uploaded".format(instance_ip, attachment),
                        as_user=True)


        time.sleep(1)
