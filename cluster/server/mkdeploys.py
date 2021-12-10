import sys, os
sys.path.append(os.getcwd()+"/..")
from utils import DeploymentWriter

class ServerDeploymentWriter(DeploymentWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def replace_placeholders(self, config, name, text):
        text = text.replace("NODE_PLACEHOLDER", config["node"])
        text = text.replace("NAME_PLACEHOLDER", name)
        text = text.replace("REDI_PLACEHOLDER", config["redi"])
        text = text.replace("INTF_PLACEHOLDER", config["interface"])
        text = text.replace("PORT_PLACEHOLDER", config["port"])
        text = text.replace("VLAN_PLACEHOLDER", config["vlan"])
        return text

if __name__ == "__main__":
    server_configs = [
        {
            "node": "nrp-01.nrp-nautilus.io", 
            "port": "2094",
            "interface": "enp2s0f0",
            "vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c170",
            "redi": "[2607:f720:1720:e00e:ec4:7aff:febb:c04e]:9001"
        }, 
        {
            "node": "nrp-01.nrp-nautilus.io", 
            "port": "2095",
            "interface": "enp2s0f1",
            "vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c171",
            "redi": "[2607:f720:1720:e00e:ec4:7aff:febb:c04f]:9002"
        }, 
    ]
    deployment_writer = ServerDeploymentWriter(
        base_dir="servers", 
        template_dir="templates", 
        app_name="rucio-sense-server", 
        configs=server_configs
    )
    deployment_writer.write()
