import os
import subprocess
import boto3



openssh = "C:\\Windows\\System32\\OpenSSH\\"

instance = {
    "instance": {
        "hostname": "i-xxxxxxxxxxxxxxxxx"
    },
    "az": {
        "hostname": "ap-southeast-2b"
    },
    "ip": {
        "hostname": "x.x.x.x"
    },
    "region": {
        "hostname": "ap-southeast-2"
    },
}



def keygen():
    cmd = "ssh-keygen -t rsa -f sshkey"
    os.system(cmd)
    
    file = open("sshkey.pub")
    line = file.read() #.replace("\n", " ")
    file.close()

    return line


def sendpub(key, instance, az):
    response = client.send_ssh_public_key(
        InstanceId=instance,
        InstanceOSUser='ubuntu',
        SSHPublicKey=key,
        AvailabilityZone=az
    )
    print(response)


def convertppk():
    cmd = "puttygen sshkey -o sshkey.ppk"
    os.system(cmd)



def runputty(ip):

    p = subprocess.Popen(['putty.exe', '-i', 'sshkey.ppk', 'ubuntu@'+ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)


if __name__ == "__main__":

    vm = input("Server: ")

    client = boto3.client('ec2-instance-connect', region_name=instance["region"][vm])

    print("Generating Key")
    key = keygen()

    print("Sending public key to AWS")
    sendpub(key,instance["instance"][vm], instance["az"][vm])

    print("Conveting PEM to PPK")
    convertppk()

    print("Launching PuTTY")
    runputty(instance["ip"][vm])


