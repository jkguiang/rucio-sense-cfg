import os
import glob

class DeploymentWriter:
    def __init__(self, base_dir, template_dir, app_name, configs=[], namespace=""):
        self.base_dir = base_dir
        self.template_dir = template_dir
        self.deployment_dir = f"{base_dir}/deployments"
        self.app_name = app_name
        self.namespace = namespace
        self.configs = configs

    def add_config(self, new_config):
        self.configs.append(new_config)
        self._check_configs()

    def write(self):
        self._check_configs()
        os.makedirs(self.base_dir, exist_ok=True)
        for old_deployment in self._get_deployments():
            for f in glob.glob(f"{old_deployment}/*"):
                os.remove(f)
            os.rmdir(old_deployment)

        for config in self.configs:
            name = self._get_deployment_name(config)
            self._write_deployment(config, name)

        with open(f"{self.base_dir}/Makefile", "w") as f_out:
            f_out.write("delete:\n")
            for new_deployment in self._get_deployments():
                local_path = new_deployment.replace(f"{self.base_dir}/", "")
                delete_cmd = f"\t- kubectl delete -k ./{local_path}"
                if self.namespace != "":
                    delete_cmd += f" -n {self.namespace}"
                f_out.write(f"{delete_cmd}\n")
            f_out.write("create:\n")
            for new_deployment in self._get_deployments():
                local_path = new_deployment.replace(f"{self.base_dir}/", "")
                apply_cmd = f"\t- kubectl apply -k ./{local_path}"
                if self.namespace != "":
                    apply_cmd += f" -n {self.namespace}"
                f_out.write(f"{apply_cmd}\n")

    def _get_deployment_name(self, config):
        N = config["node"].split(".")[0].split("-")[-1]
        return f"{self.app_name}-{N}-{config['interface'].replace('.', '-')}"

    def _strip_comments(self, extension, text):
        if extension in ("yaml", "cfg"):
            return "\n".join([l for l in text.split("\n") if l.strip()[:1] != "#"])
        else:
            return text

    def _replace_placeholders(self, config, name, text):
        raise NotImplementedError

    def _check_configs(self):
        if len(self.configs) > 1:
            for i, cfg in enumerate(self.configs[:-1]):
                assert cfg.keys() == self.configs[i+1].keys()

    def _get_deployments(self):
        return [d for d in glob.glob(f"{self.deployment_dir}/*")]

    def _write_deployment(self, config, name):
        os.makedirs(f"{self.deployment_dir}/{name}", exist_ok=True)
        for template in glob.glob(f"{self.template_dir}/*"):
            with open(template, "r") as f_in:
                text = f_in.read()
                text = self._strip_comments(template.split(".")[-1], text)
                text = self._replace_placeholders(config, name, text)
            with open(f"{self.deployment_dir}/{name}/{template.split('/')[-1]}", "w") as f_out:
                f_out.write(text)

