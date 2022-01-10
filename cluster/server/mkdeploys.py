import sys, os
from subprocess import Popen, PIPE
sys.path.append(os.getcwd()+"/..")
from utils import DeploymentWriter

class ServerDeploymentWriter(DeploymentWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _replace_placeholders(self, config, name, text):
        text = text.replace("NODE_PLACEHOLDER", config["node"])
        text = text.replace("NAME_PLACEHOLDER", name)
        text = text.replace("REDI_VLAN_PLACEHOLDER", config["redi_vlan"])
        text = text.replace("REDI_PORT_PLACEHOLDER", config["redi_port"])
        text = text.replace("INTF_PLACEHOLDER", config["interface"])
        text = text.replace("PORT_PLACEHOLDER", config["port"])
        text = text.replace("VLAN_PLACEHOLDER", config["vlan"])
        return text

    def _get_deployment_name(self, config):
        N = config["node"].split(".")[0].split("-")[-1]
        return f"{self.app_name}-{N}-{config['port'].replace('.', '-')}"

    def make_certs(self):
        if len(self._get_deployments()) == 0:
            print("WARNING: No certs made; run write() first!")
            return
        for config in self.configs:
            base_dir = f"{os.getcwd()}/{self.deployment_dir}/{self._get_deployment_name(config)}"
            cmd = f"../certs/generate.sh {config['vlan']} {base_dir}"
            Popen(cmd.split(), cwd="../certs", stdout=PIPE).communicate()

if __name__ == "__main__":
    server_configs = [
        {
            "node": "nrp-01.nrp-nautilus.io", 
            "vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c171",
            "port": "2094",
            "interface": "enp2s0f1",
            "redi_vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c04f",
            "redi_port": "9001"
        }, 
        {
            "node": "nrp-01.nrp-nautilus.io", 
            "vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c173",
            "port": "2095",
            "interface": "enp2s0f1",
            "redi_vlan": "2607:f720:1720:e00e:ec4:7aff:febb:c050",
            "redi_port": "9002"
        }, 
    ]
    deployment_writer = ServerDeploymentWriter(
        base_dir="./", 
        template_dir="templates", 
        app_name="rucio-sense-server", 
        configs=server_configs
    )
    deployment_writer.write()
    deployment_writer.make_certs()
