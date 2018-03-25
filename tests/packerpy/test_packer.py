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


class TestPackerExecutable(object):
    """
    TODO these are currently integration tests, requiring packer binary available
    """

    def test_command_build(self):
        result = PackerExecutable(machine_readable=False).build(self.get_test_template("cmd_validate_good.json"),
                                                                color=False)

        assert result[0] == 1, result

    def test_command_inspect(self):
        result = PackerExecutable().inspect(self.get_test_template("cmd_validate_good.json"))

        assert result[0] == 0, result

    def test_command_validate_syntax_only(self):
        result = PackerExecutable().validate(self.get_test_template("cmd_validate_good.json"), syntax_only=True)

        assert result[0] == 0, result

    def test_command_validate(self):
        result = PackerExecutable().validate(self.get_test_template("cmd_validate_good.json"))

        assert result[0] == 1, result
        assert "Bad script 'setup_things.sh':" in result[1], result

    def test_command_version(self):
        result = PackerExecutable().version()
        assert result[0] == 0, result
        assert 'Packer v' in result[1], result

    def test_template_json(self):
        result = PackerExecutable().validate("""{
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
        }
        """, syntax_only=True)

        assert result[0] == 0, result

    def test_template_file(self):
        result = PackerExecutable().validate(self.get_test_template("cmd_validate_good.json"), syntax_only=True)

        assert result[0] == 0, result

    def test_config_override(self):
        result = PackerExecutable(machine_readable=False, config={'stdout': None}).version()

        assert result[0] == 0, result
        assert result[1] is None, result

    def get_test_template(self, file_name):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates/{}".format(file_name))
