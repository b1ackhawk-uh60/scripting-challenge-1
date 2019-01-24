import boto3
from pprint import pprint

#assume role aws
sts_client = boto3.client('sts')
assumed_role_object=sts_client.assume_role(RoleArn="arn:aws:iam::[protected]:role/ops-challenge-role-to-assume",RoleSessionName="AssumeRoleSession1")
credentials=assumed_role_object['Credentials']
ec2_client=boto3.client('ec2',region_name='us-east-1',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],)
response = ec2_client.describe_instances(Filters=[{'Name':'tag:monitored_instance','Values':['True']}])

#create dictionary to store required info for nagios definitions
instancedict = {}
for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
                instancedict[instance["InstanceId"]] = {}
                instancedict[instance["InstanceId"]]['PrivateIp'] = instance['PrivateIpAddress']
                for tag in instance["Tags"]:
                        instancedict[instance["InstanceId"]][tag['Key']] = tag['Value']

#output nagios definitions
for instance in instancedict:
    if instancedict[instance]['environment'] == 'production':
        criticality = 'critical'
    else:
        criticality = 'noncritical'
    duse = "server"
    host_name = instancedict[instance]['Name']
    hostgroups = "{0}-{1}".format(instancedict[instance]['monitored_service'],criticality)
    cg1 = "ops-{0}".format(criticality)
    cg2 = "web-{0}".format(criticality)
    address = instancedict[instance]['PrivateIp']
    suse = "default-service"
    service_description = "all-disks-{0}-{1}".format(instancedict[instance]['monitored_service'],criticality)
    check_command = "check_all_disks"
    nl = '\n'
    tb = '\t'
    print("define host {{{nl}\
    {tb}use{tb}{tb}{tb}{duse}{nl}\
    {tb}host_name{tb}{tb}{host_name}{nl}\
    {tb}hostgroups{tb}{tb}{hostgroups}{nl}\
    {tb}contact_groups{tb}{tb}{cg1},{cg2}{nl}\
    {tb}address{tb}{tb}{tb}{address}{nl}\
    }}".format(**locals()))
    print("define service {{{nl}\
    {tb}use{tb}{tb}{tb}{suse}{nl}\
    {tb}service-description{tb}{service_description}{nl}\
    {tb}host_name{tb}{tb}{host_name}{nl}\
    {tb}check_command{tb}{tb}{check_command}{nl}\
    {tb}contact_groups{tb}{tb}{cg1},{cg2}{nl}\
    }}".format(**locals()))
