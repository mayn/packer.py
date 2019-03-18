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
import logging
import platform
import subprocess


class PackerExecutable(object):
    """
    wrapper for executing packer CLI commands
    see https://www.packer.io/docs/commands/build.html

    """
    PATH = 'executable_path'

    def __init__(self, executable_path=None, machine_readable=True, config=None):
        """

        :param machine_readable:
        :param config:
        """
        self.log = logging.getLogger(self.__class__.__name__)
        # default configuration
        self.configuration = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            PackerExecutable.PATH: 'packer.exe' if 'Windows' == platform.system() else '/usr/local/packer'
        }

        # add overrides
        if executable_path:
            self.configuration[PackerExecutable.PATH] = executable_path

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

    @staticmethod
    def _explode_args(**kwargs):
        exploded = list()
        for (key, value) in kwargs.items():
            if '_' in key:
                key = key.replace("_", "-")
            if value is True:
                exploded.append("-{}".format(key))
            elif isinstance(value, dict):
                for (k, v) in value.items():
                    exploded.append("-{}".format(key))
                    exploded.append("{}={}".format(k, v))
            else:
                exploded.append("-{}={}".format(key, value))

        return exploded

    def execute_cmd(self, packer_cmd, template=None, **kwargs):
        cmd_args = list()
        cmd_args.append(self.configuration[PackerExecutable.PATH])
        cmd_args.append(packer_cmd)

        if 'machine-readable' in self.configuration:
            cmd_args.append('-machine-readable')

        cmd_args.extend(self._explode_args(**kwargs))

        is_json = template and template.strip("\n\t ").startswith('{')
        if template:
            if is_json:
                cmd_args.append('-')
            else:
                cmd_args.append(template)

        p = subprocess.Popen(cmd_args, stdin=subprocess.PIPE if is_json else None,
                             stdout=self.configuration['stdout'], stderr=self.configuration['stderr'])
        out, err = p.communicate(template.encode('utf-8') if is_json else None)

        return p.returncode, out, err
