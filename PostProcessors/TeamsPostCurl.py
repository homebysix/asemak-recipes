#!/usr/bin/python
#
# Copyright 2020 Andy Semak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from autopkglib import Processor, ProcessorError, URLGetter

# Set the webhook_url to the one provided by Teams when you create the webhook

__all__ = ["TeamsPostCurl"]


class TeamsPost(Processor):
    description = (
        "Posts to Teams via webhook based on output of a MunkiImporter. "
        "Teams alternative to the post processor provided by Ben Reilly "
        "(@notverypc) "
        "Based on Graham Pugh's slacker.py - "
        "https://github.com/grahampugh/recipes/blob/master/PostProcessors/slacker.py"  # noqa
        "and "
        "@thehill idea on macadmin slack - "
        "https://macadmins.slack.com/archives/CBF6D0B97/p1542379199001400 "
        "Takes elements from "
        "https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784"
        "and "
        "https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py")  # noqa

    input_variables = {
        "munki_info": {
            "required": False,
            "description": ("Munki info dictionary to use to display info.")
        },
        "munki_repo_changed": {
            "required": False,
            "description": ("Whether or not item was imported.")
        },
        "webhook_url": {
            "required": False,
            "description": ("Teams webhook.")
        }
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):
        was_imported = self.env.get("munki_repo_changed")
        munkiInfo = self.env.get("munki_info")
        webhook_url = self.env.get("webhook_url")
        emoji = ":rocket:"

        if was_imported:
            name = self.env.get("munki_importer_summary_result")[
                "data"]["name"]
            version = self.env.get("munki_importer_summary_result")[
                "data"]["version"]
            pkg_path = self.env.get("munki_importer_summary_result")[
                "data"]["pkg_repo_path"]
            pkginfo_path = self.env.get("munki_importer_summary_result")[
                "data"]["pkginfo_path"]
            catalog = self.env.get("munki_importer_summary_result")[
                "data"]["catalogs"]
            if name:
                teams_text = "**New item added to repo:**   \nTitle: **%s**\
                             \nVersion: **%s**  \nCatalog: **%s**  \nPkg Path:\
                             **%s**  \nPkginfo Path: **%s**" % (
                             name, version, catalog, pkg_path,
                             pkginfo_path)
                teams_data = {'text': teams_text, 'textformat': "markdown",
                              'title': "%s" % (emoji)}
            
            # Build the headers
            headers = {
              "accept": "application/json",
              "Content-Type": "application/x-www-form-urlencoded"
            }

            # Build the required curl switches
            curl_opts = [
                "--url", "{}".format(token_url),
                "--request", "POST",
                "--data", "client_id={client_id}&client_secret={client_secret}".format(client_id=client_id, client_secret=client_secret)
            ]

            try:
              # Initialize the curl_cmd, add the curl options, and execute the curl
              curl_cmd = self.prepare_curl_cmd()
              self.add_curl_headers(curl_cmd, headers)
              curl_cmd.extend(curl_opts)
              # response_token = self.download_with_curl(curl_cmd)

        except:
            raise ProcessorError("Failed to acquire bearer authentication token!)

if __name__ == "__main__":
    processor = TeamsPostCurl()
    processor.execute_shell()