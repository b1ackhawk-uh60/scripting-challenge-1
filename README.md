# scripting_challenge_1
A scripting challenge that involved polling aws for resources and then creating nagios core definitions based off defined criteria

Instructions:
Write a python script that uses the python aws api (boto3) to discover monitored instances and
generate Nagios host and service definitions as described below.
Examples are provided, no experience with Nagios is required.
Role allowing discovery via python api:
● arn:aws:iam::[protected]:role/ops-challenge-role-to-assume
This role will allow you to discover running instance. Only the instances with the tag
Key=monitored_instance, Value=True as well as the instance you have been provided are
pertinent to this challenge. Any other instances should be ignored.

For each instance tagged with key=monitored_instance, value=True you should output a Nagios
Host definition as well as a Nagios Service definition for the service running on that instance.
To determine the type of service, inspect the monitored_service tag for the instance.
In order to determine criticality (critical vs noncritical) inspect the environment tag: items tagged
production are critical others are non critical
In addition, you should determine if the current configuration of each monitored instance is
sufficient for monitoring via the Nagios NRPE port (5666) from the instance you have been
provided. If any changes are required, you should note those, either in your output or a
follow-up email. Be as specific as possible.
Example host and service definitions:
# Host definition for instance tagged with Name=web1, environment=production,
monitored_service=web
define host {
use server
host_name web1
hostgroups web-critical
contact_groups ops-critical,web-critical
address <address of instance used for NRPE traffic>
}
# Service definition for service on the above host
define service {
use default-service
service_description all-disks-web-critical
host_name web1
check_command check_all_disks
contact_groups ops-critical,web-critical
}
# Note: For those familiar with Nagios, you can assume the existence of the following resources
which are used in the above.

● Host definition with name: server
● Service definition with name: default-service

● Hostgroup definitions for web-critical, web-noncritical, and any other hostgroups
required, for example backend-critical for a host tagged with
monitored_service=backend and environment=production
