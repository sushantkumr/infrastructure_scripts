import boto3
import jmespath


region = "us-east-1"
boto3.setup_default_session(profile_name="personal")
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

        response = ec2_client.describe_instances(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )
        instance_list = response["Reservations"]

        for instance_obj in instance_list:
            instance = instance_obj["Instances"][0]
            if instance["InstanceType"] == "m5.large":
                search_string = "[?Key == 'Name'].Value"
                instance_name = jmespath.search(search_string, instance["Tags"])
                m5_large_instances[instance["InstanceId"]] = instance_name

        print(m5_large_instances)
    except Exception as e:
        print(f"Exception encountered while running: {e}")
