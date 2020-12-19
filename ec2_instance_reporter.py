import boto3
import jmespath


region = "us-east-1"
boto3.setup_default_session(profile_name="personal")
ec2 = boto3.resource("ec2", region)
ec2_client = boto3.client("ec2", region_name=region)

if __name__ == "__main__":
    try:
        m5_large_instances = {}

        response = ec2_client.describe_vpcs(
            Filters=[
                {
                    "Name": "isDefault",
                    "Values": [
                        "true",
                    ],
                },
            ]
        )

        vpc_id = response["Vpcs"][0]["VpcId"]

        response = ec2.instances.filter(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )
        for instance in response:
            if instance.instance_type == "m5.large":
                search_string = "[?Key == 'Name'].Value"
                instance_name = jmespath.search(search_string, instance.tags)
                m5_large_instances[instance.id] = instance_name

        print(m5_large_instances)
    except Exception as e:
        print(f"Exception encountered while running: {e}")
