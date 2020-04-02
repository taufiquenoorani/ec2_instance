import boto3
import argparse
import os
import time

region = ''
access_key = ''
secret_key = ''

# Create EC2 Instance
def create_ec2_instance():
    # Logging into EC2 environment
    ec2 = boto3.resource('ec2', region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # Get name of new key_pair
    key_pair = input('Enter the name of your new key pair: ')
    with open(key_pair, 'w') as keyfile:
        new_key = ec2.create_key_pair(KeyName=key_pair)
        KeyPairOut = str(new_key.key_material)
        keyfile.write(KeyPairOut)
        os.chmod(key_pair, 0o400)


    local_path = input('Please enter the local path to file: ')
    ami_id = input('Please enter the AMI ID: ')
    print('Authentication Successful. Creating an instance now..')

    # Create instance
    instances = ec2.create_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        KeyName=key_pair,
        InstanceType='t2.micro')

    # Transfer file to remote server
    for instance in instances:
        instance.wait_until_running()
        instance.reload()

        print("Instance IP: %s" % instance.public_ip_address)
        instance_ip = instance.public_ip_address

        time.sleep(2)

        print('Transferring files...')

        time.sleep(2)

        # Upload the file
        os.system('/usr/bin/rsync -Pav -e "ssh -i %s -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -q" %s ubuntu@%s:~' %(key_pair, local_path, instance_ip))
        
        # This can be replaced with line 51 if you would like to transfer and unzip the file at the same time.
        # os.system('cat %s | ssh -i %s -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q ubuntu@%s "mkdir webapp && cd ~/webapp; tar zxvf -"' %(local_path, key_pair_path, instance_ip))
        
# Get arguments from the terminal
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('region', help='Region')
    parser.add_argument('access_key', help='Access Key')
    parser.add_argument('secret_key', help='Secret Key')
    args = parser.parse_args()
    global region
    global access_key
    global secret_key
    region = args.region
    access_key = args.access_key
    secret_key = args.secret_key
    create_ec2_instance()

if __name__ == '__main__': main()
