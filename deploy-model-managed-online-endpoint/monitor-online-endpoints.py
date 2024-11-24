#invokes an endpoint and displays the response

# test the blue deployment with sample data
response = ml_client.online_endpoints.invoke(
    endpoint_name=online_endpoint_name,
    deployment_name="blue",
    request_file="sample-data.json",
)

if response[1]=='1':
    print("Yes")
else:
    print ("No")


