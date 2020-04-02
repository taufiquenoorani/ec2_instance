<h2> EC2 Instance </h2>
Create new EC2 instance and upload files to it.

<h3>Prerequisites:</h3>
<ol>
<li> Python 3+ </li>
<li> pip install boto3 </li>
<li> AWS access key ID and secret access key (https://console.aws.amazon.com/iam/home#/users) </li>
<li> Region name (http://docs.aws.amazon.com/general/latest/gr/rande.html) </li>
</ol>

<h3>Installation:</h3>
<ol>
<li> Clone the repo </li>
<li> Run the script by executing ec2_instance.py along with the arguments </li>
  <code>python ec2_instance.py region aws_access_key_id aws_secret_access_key</code>
<li> It will ask you to create a new key pair to connect to your EC2 instance </li>
<li> Enter the name of the new key_pair </li>
<li> Enter the name of the local file path (that needs to be uploaded) </li>
<li> Enter an existing AMI ID </li>
</ol>

<h3>How it works?</h3>
The script will collect your credentials and create a new micro EC2 instance. It will wait until the system state is running and get the public IP address of the instance. The script will rsync the file from your local path to the remote host using the key_pair and upload it under the home directory of ubuntu user


<h3>Author:</h3>
@taufique786
