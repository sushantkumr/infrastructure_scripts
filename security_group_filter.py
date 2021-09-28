import boto3

client = boto3.client('ec2')

response = client.describe_security_groups()
security_groups = response['SecurityGroups']

faulty_sgs = []

def is_rule_open_to_all(rule):
    ip_range = rule['IpRanges']
    if ip_range:
        if ip_range[0]['CidrIp'] == "0.0.0.0/0":
            faulty_sgs.append(sg['GroupName'])
    ipv6_range = rule['Ipv6Ranges']
    if ipv6_range:
        if ipv6_range[0]['CidrIpv6'] == '::/0':
            faulty_sgs.append(sg['GroupName'])

for sg in security_groups:
    list_of_ingress_rules = sg['IpPermissions']
    for rule in list_of_ingress_rules:
        if 'FromPort' in rule:
            if rule["FromPort"] == 22 and rule["ToPort"] == 22:
                is_rule_open_to_all(rule)
            if rule["FromPort"] <= 22 and rule["ToPort"] >= 22 and rule["FromPort"] != rule["ToPort"]:
                is_rule_open_to_all(rule)
        elif rule['IpProtocol'] == "-1":
            is_rule_open_to_all(rule)
print(faulty_sgs)
