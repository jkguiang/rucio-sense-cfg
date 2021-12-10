import sys, os
sys.path.append(os.getcwd()+"/..")
from utils import DeploymentWriter

class RediDeploymentWriter(DeploymentWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def replace_placeholders(self, config, name, text):
        text = text.replace("NODE_PLACEHOLDER", config["node"])
        text = text.replace("NAME_PLACEHOLDER", name)
        text = text.replace("INTF_PLACEHOLDER", config["interface"])
        text = text.replace("MAIN_PORT_PLACEHOLDER", config["main_port"])
        text = text.replace("REDI_PORT_PLACEHOLDER", config["redi_port"])
        text = text.replace("VLAN_PLACEHOLDER", config["vlan"])
        return text

if __name__ == "__main__":
    redi_configs = [
        {
            "node": "nrp-02.nrp-nautilus.io", 
            "main_port": "2094",
            "redi_port": "9001",
            "interface": "enp2s0f0",
            "vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c04e",
        }, 
        {
            "node": "nrp-02.nrp-nautilus.io", 
            "main_port": "2095",
            "redi_port": "9002",
            "interface": "enp2s0f1",
            "vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c04f",
        }, 
    ]
    deployment_writer = RediDeploymentWriter(
        base_dir="redis", 
        template_dir="templates", 
        app_name="rucio-sense-redi", 
        configs=redi_configs
    )
    deployment_writer.write()
