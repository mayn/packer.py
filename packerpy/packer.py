"""
Copyright 2018 Matthew Aynalem

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import subprocess

"""
packer commands
"""


class PackerExecutable(object):
    """
    wrapper for executing packer CLI commands
    see https://www.packer.io/docs/commands/build.html

    """

    def __init__(self, machine_readable=True, config=None):
        """

        :param machine_readable:
        :param config:
        """

        # default configuration
        self.configuration = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'executable_path': '/usr/local/packer'
        }

        # add overrides
        if config:
            self.configuration.update(config)

        if machine_readable:
            self.configuration['machine-readable'] = True

    def build(self, template, **kwargs):
        """
        https://www.packer.io/docs/commands/build.html

        :param template:
        :param kwargs:
        :return:
        """
        return self.execute_cmd("build", template, **kwargs)

    def inspect(self, template, **kwargs):
        """
        https://www.packer.io/docs/commands/inspect.html

        :param template:
        :param kwargs:
        :return:
        """
        return self.execute_cmd("inspect", template, **kwargs)

    def validate(self, template, **kwargs):
        """
        https://www.packer.io/docs/commands/validate.html

        :param template:
        :param kwargs:
        :return:
        """
        return self.execute_cmd("validate", template, **kwargs)

    def version(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.execute_cmd("version", **kwargs)

    def execute_cmd(self, packer_cmd, template=None, **kwargs):
        cmd_args = list()
        cmd_args.append(self.configuration['executable_path'])
        cmd_args.append(packer_cmd)

        if 'machine-readable' in self.configuration:
            cmd_args.append('-machine-readable')

        for key, value in list(kwargs.items()):
            if '_' in key:
                key = key.replace("_", "-")
            if value is True:
                cmd_args.append("-{}".format(key))
            else:
                cmd_args.append("-{}={}".format(key, value))

        is_json = template and template.startswith('{')
        if template:
            if is_json:
                cmd_args.append('-')
            else:
                cmd_args.append(template)

        p = subprocess.Popen(cmd_args, stdin=subprocess.PIPE if is_json else None,
                             stdout=self.configuration['stdout'], stderr=self.configuration['stderr'])
        out, err = p.communicate(template.encode('utf-8') if is_json else None)

        return p.returncode, out, err
