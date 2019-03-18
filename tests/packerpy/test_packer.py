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

import os
import pytest
from packerpy import PackerExecutable
from collections import OrderedDict


class TestPackerExecutable(object):
    """
    TODO these are currently integration tests, requiring packer binary available
    """

    def test_command_build(self):
        result = PackerExecutableWrapper(machine_readable=False) \
            .build(self.get_test_template("cmd_validate_good.json"),
                   color=False)

        assert result[0] == 1, result

    def test_command_inspect(self):
        result = PackerExecutableWrapper().inspect(self.get_test_template("cmd_validate_good.json"))

        assert result[0] == 0, result

    def test_command_validate_syntax_only(self):
        result = PackerExecutableWrapper().validate(self.get_test_template("cmd_validate_good.json"), syntax_only=True)

        assert result[0] == 0, result

    def test_command_validate(self):
        result = PackerExecutableWrapper().validate(self.get_test_template("cmd_validate_good.json"))

        assert result[0] == 1, result
        assert "Bad script 'setup_things.sh':" in str(result[1]), result

    def test_command_version(self):
        result = PackerExecutableWrapper().version()
        assert result[0] == 0, result
        assert 'Packer v' in str(result[1]), result

    def test_template_json(self):
        template = """
        {
          "builders": [
            {
              "type": "amazon-ebs",
              "access_key": "...",
              "secret_key": "...",
              "region": "us-east-1",
              "source_ami": "ami-fce3c696",
              "instance_type": "t2.micro",
              "ssh_username": "ubuntu",
              "ami_name": "packer {{timestamp}}"
            }
          ],

          "provisioners": [
            {
              "type": "shell",
              "inline": ["echo foo"]
            }
          ]
        }"""
        result = PackerExecutableWrapper().validate(template, syntax_only=True)

        assert result[0] == 0, result

    def test_template_file(self):
        result = PackerExecutableWrapper().validate(self.get_test_template("cmd_validate_good.json"), syntax_only=True)

        assert result[0] == 0, result

    def test_specify_executable_path(self):
        p = PackerExecutable(executable_path="/usr/local/bin/packer")
        result = p.configuration

        assert result[PackerExecutable.PATH] == "/usr/local/bin/packer", result

    def test_config_override(self):
        result = PackerExecutableWrapper(machine_readable=False, config={'stdout': None}).version()

        assert result[0] == 0, result
        assert result[1] is None, result

    def test_multiple_var_arguments(self):
        packer = PackerExecutableWrapper(machine_readable=False, config={'stdout': None})
        template = """
            {
              "builders": [
                {
                  "type": "null",
                  "ssh_host":     "127.0.0.1",
                  "ssh_username": "foo",
                  "ssh_password": "bar"
                }
              ]
            }
        """
        result = packer.validate(template, var=OrderedDict([('aws_access_key', 'bar'), ('aws_secret_key', 'baz')]))

        assert result[0] == 0, result
        assert result[1] is None, result

    def test_explode_args_dict(self):
        packer = PackerExecutableWrapper()

        result = packer._explode_args(var=OrderedDict([('aws_access_key', 'YOUR KEY'),
                                                       ('aws_secret_key', 'foo'),
                                                       ('region', 'us-east-1')]))

        assert len(result) == 6, result
        assert ' '.join(result) == "-var aws_access_key=YOUR KEY -var aws_secret_key=foo -var region=us-east-1"

    @pytest.mark.parametrize("test_kwargs,expected", [
        ({'force': True}, "-force"),
        ({'color': False}, "-color=False"),
    ])
    def test_explode_args_boolean(self, test_kwargs, expected):
        packer = PackerExecutableWrapper()

        result = packer._explode_args(**test_kwargs)
        assert ' '.join(result) == expected

    def get_test_template(self, file_name):
        print(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "templates", file_name))
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "templates", file_name)


class PackerExecutableWrapper(PackerExecutable):
    """
    wrapper for testing
    """

    def __init__(self, machine_readable=True, config=None):
        if config is None:
            config = {}

        executable_path=os.getenv('PACKER_EXECUTABLE')

        super(PackerExecutableWrapper, self).__init__(executable_path, machine_readable, config)
