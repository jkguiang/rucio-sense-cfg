import sys, os
from subprocess import Popen, PIPE
sys.path.append(os.getcwd()+"/..")
from utils import DeploymentWriter

class RediDeploymentWriter(DeploymentWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _replace_placeholders(self, config, name, text):
        text = text.replace("SITE_PLACEHOLDER", self._get_site_name(config))
        text = text.replace("NODE_PLACEHOLDER", config["node"])
        text = text.replace("NAME_PLACEHOLDER", name)
        text = text.replace("INTF_PLACEHOLDER", config["interface"])
        text = text.replace("MAIN_PORT_PLACEHOLDER", config["main_port"])
        text = text.replace("REDI_PORT_PLACEHOLDER", config["redi_port"])
        text = text.replace("IPV6_PLACEHOLDER", config["ipv6"])
        return text

    def _get_deployment_name(self, config):
        N = config["node"].split(".")[0].split("-")[-1]
        return f"{self.app_name}-{N}-{config['main_port'].replace('.', '-')}"

    def _get_site_name(self, config):
        ipv6_last4 = config["ipv6"].split(":")[-1]
        return f"RUCIO_SENSE_REDI_{ipv6_last4}_{config['main_port']}_{config['redi_port']}"

    def make_certs(self):
        if len(self._get_deployments()) == 0:
            print("WARNING: No certs made; run write() first!")
            return
        for config in self.configs:
            base_dir = f"{os.getcwd()}/{self.deployment_dir}/{self._get_deployment_name(config)}"
            cmd = f"../certs/generate.sh {config['ipv6']} {base_dir}"
            Popen(cmd.split(), cwd="../certs", stdout=PIPE).communicate()

if __name__ == "__main__":
    redi_configs = [
        {
            "node": "nrp-01.nrp-nautilus.io", 
            "main_port": "2094",
            "redi_port": "9001",
            "interface": "macvlan0",
            "ipv6": "2607:f720:1720:e00e:ec4:7aff:febb:c171",
        }, 
        {
            "node": "nrp-01.nrp-nautilus.io", 
            "main_port": "2095",
            "redi_port": "9002",
            "interface": "macvlan1",
            "ipv6": "2607:f720:1720:e00e:ec4:7aff:febb:c172",
        }, 
        {
            "node": "nrp-01.nrp-nautilus.io", 
            "main_port": "2096",
            "redi_port": "9003",
            "interface": "macvlan2",
            "ipv6": "2607:f720:1720:e00e:ec4:7aff:febb:c173",
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
