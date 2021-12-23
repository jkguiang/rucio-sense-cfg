import sys, os
from subprocess import Popen, PIPE
sys.path.append(os.getcwd()+"/..")
from utils import DeploymentWriter

class RediDeploymentWriter(DeploymentWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _replace_placeholders(self, config, name, text):
        text = text.replace("NODE_PLACEHOLDER", config["node"])
        text = text.replace("NAME_PLACEHOLDER", name)
        text = text.replace("INTF_PLACEHOLDER", config["interface"])
        text = text.replace("MAIN_PORT_PLACEHOLDER", config["main_port"])
        text = text.replace("REDI_PORT_PLACEHOLDER", config["redi_port"])
        text = text.replace("VLAN_PLACEHOLDER", config["vlan"])
        return text

    def make_certs(self):
        if len(self._get_deployments()) == 0:
            print("WARNING: No certs made; run write() first!")
            return
        for config in self.configs:
            base_dir = f"{os.getcwd()}/{self.deployment_dir}/{self._get_deployment_name(config)}"
            cmd = f"../certs/generate.sh {config['vlan']} {base_dir}"
            Popen(cmd.split(), cwd="../certs", stdout=PIPE).communicate()

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
        base_dir="./", 
        template_dir="templates", 
        app_name="rucio-sense-redi", 
        configs=redi_configs
    )
    deployment_writer.write()
    deployment_writer.make_certs()
