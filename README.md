# infrastructure_scripts
Scripts written to provision infrastructure

The repo contains 2 scripts meant to deploy and find out information about the underlying infrastructure in an AWS account. Before running any of them, the first step would be to install packages into a python virtual environment. Follow the steps below after cloning the repository.

### Create a python virtual environment
1. virtualenv python3.9 venv_infrastructure
2. source ./venv_infrastructure/bin/activate
3. git clone git@github.com:sushantkumr/infrastructure_scripts.git
4. cd infrastructure_scripts
5. pip install requirements.txt

#### ec_instance_reporter.py
Script to report all EC2 machines in a default VPC which have instance type as m5.large.
The script can be run by executing the following command

> How to run the script (AWS_PROFILE is the profile you wish to run the script for)

python ec2_instance_reporter.py AWS_PROFILE


#### launch_instances.yaml

> How to create the stack. This requires AWS CLI to be installed on your system. [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

aws cloudformation create-stack --stack-name prod-stack --template-body file://launch_instances.yaml --parameters ParameterKey="ProdVPC",ParameterValue="VPC_ID" ParameterKey=PrivateSubnet1CIDR,ParameterValue="SUBNET_CIDR_BLOCK"

```
aws ec2 describe-vpcs \
    --filters Name=isDefault,Values=true \
    --query 'Vpcs[*].VpcId' \
    --output text
```

VPC_ID -- can be found by running the above snippet on your system; replace VPC_ID with `VpcId`
SUBNET_CIDR_BLOCK -- can be computed from the output of the above snippet. If your VPC CIDR block is `192.168.0.0/16`, the subnet's CIDR block can be `192.168.10.0/20`
