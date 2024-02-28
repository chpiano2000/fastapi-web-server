import os

from dotenv import load_dotenv
from fastapi import FastAPI
from kubernetes import client, config

try:
    config.load_kube_config()
except:
    # load_kube_config throws if there is no config, but does not document what it throws, so I can't rely on any particular type here
    config.load_incluster_config()

load_dotenv()
app = FastAPI()

v1 = client.CoreV1Api()

@app.get("/{namespace}")
async def root(namespace: str):
    services_pods_info = []
    
    # Get all services in the cluster
    services = v1.list_namespaced_service(namespace).items
    for service in services:
        service_info = {
            "service_name": service.metadata.name,
            "service_namespace": service.metadata.namespace,
            "service_type": service.spec.type,
            "service_ports": [{
                "port": port.port,
                "target_port": port.target_port,
                "protocol": port.protocol
            } for port in service.spec.ports],
            "endpoints": [],
        }
        # Get endpoints for the service
        endpoints = v1.list_namespaced_endpoints(namespace=service_info["service_namespace"], field_selector=f"metadata.name={service_info['service_name']}").items
        for ep in endpoints:
            for subset in ep.subsets:
                for address in subset.addresses:
                    for port in subset.ports:
                        endpoint_data = {
                            "ip": address.ip,
                            "port": port.port,
                            "protocol": port.protocol,
                            "pod_name": None  # Initialize pod_name as None
                        }

                        # Get pod name for the current endpoint IP
                        pods = v1.list_namespaced_pod(namespace=service_info["service_namespace"], field_selector=f"status.podIP={endpoint_data['ip']}").items
                        if pods:
                            endpoint_data["pod_name"] = pods[0].metadata.name
                        
                        service_info["endpoints"].append(endpoint_data)

        services_pods_info.append(service_info)
        
    return services_pods_info


@app.get("/developer")
async def get_developer():
    return {"developer": os.getenv("DEVELOPER", "unknown")}
