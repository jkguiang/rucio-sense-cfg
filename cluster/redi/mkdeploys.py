import os
import glob
import subprocess

def write_deployment(config, name, deployment_dir="deployments", template_dir="template"):
    os.makedirs(f"{deployment_dir}/{name}", exist_ok=True)
    for template in glob.glob(f"{template_dir}/*"):
        with open(template, "r") as f_in:
            text = f_in.read()
            if template.split(".")[-1] in ("yaml", "cfg"):
                # Strip comments from templates
                text = "\n".join([l for l in text.split("\n") if l.strip()[:1] != "#"])
            # Replace placeholders
            text = text.replace("NODE_PLACEHOLDER", config["node"])
            text = text.replace("NAME_PLACEHOLDER", name)
            text = text.replace("INTF_PLACEHOLDER", config["interface"])
            text = text.replace("MAIN_PORT_PLACEHOLDER", config["main_port"])
            text = text.replace("REDI_PORT_PLACEHOLDER", config["redi_port"])
            text = text.replace("VLAN_PLACEHOLDER", config["vlan"])
        with open(f"{deployment_dir}/{name}/{template.split('/')[-1]}", "w") as f_out:
            f_out.write(text)

def write_deployments(configs, base_dir="servers", template_dir="template", server_name="origin"):
    os.makedirs(base_dir, exist_ok=True)
    deployment_dir = f"{base_dir}/deployments"
    for old_deployment in __get_deployments(deployment_dir):
        for f in glob.glob(f"{old_deployment}/*"):
            os.remove(f)
        os.rmdir(old_deployment)

    for i, config in enumerate(configs):
        N = config["node"].split(".")[0].split("-")[-1]
        write_deployment(
            config, 
            f"{server_name}-{N}-{config['interface'].replace('.', '-')}", 
            deployment_dir=deployment_dir,
            template_dir=template_dir
        )

    with open(f"{base_dir}/Makefile", "w") as f_out:
        f_out.write("delete:\n")
        for new_deployment in __get_deployments(deployment_dir):
            local_path = new_deployment.replace(f"{base_dir}/", "")
            f_out.write(f"\t- kubectl delete -k ./{local_path}\n")
        f_out.write("create:\n")
        for new_deployment in __get_deployments(deployment_dir):
            local_path = new_deployment.replace(f"{base_dir}/", "")
            f_out.write(f"\t- kubectl apply -k ./{local_path}\n")

def __get_deployments(deployment_dir="deployments"):
    return [d for d in glob.glob(f"{deployment_dir}/*")]

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
    write_deployments(redi_configs, base_dir="redis", template_dir="templates", server_name="rucio-sense-redi")
