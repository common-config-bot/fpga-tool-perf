#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018-2022 F4PGA Authors
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
#
# SPDX-License-Identifier: Apache-2.0
"""
This script is responsible for generating the HTML pages for the results
visualization generated by the FPGA tool perf CI runs.

The output of this script are the following:
    - index.html: index page containing all the reults for each device/project
    - data.js: contains historical runs' data to visualize in the corresponding
               graphs
"""

import jinja2
from argparse import ArgumentParser
import os

from generate_index_page import generate_index_html
from project_results import ProjectResults


def main():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('html'))

    parser = ArgumentParser()

    parser.add_argument(
        '-i',
        '--in-dir',
        type=str,
        help='Directory containing json data files'
    )
    parser.add_argument(
        '-o', '--out-dir', type=str, help='Save outputs in a given directory'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.in_dir):
        os.makedirs(args.in_dir)

    index_template = env.get_template('index.html')
    data_template = env.get_template('data.js')

    results = list()

    for project_name in os.listdir(args.in_dir):
        project_dir = os.path.join(args.in_dir, project_name)
        if not os.path.isdir(project_dir):
            print(f'Skipping `{project_dir}` because it' 's not a directory.')
            continue

        # Do not filter failed tests
        project_results = ProjectResults(project_name, project_dir)
        results.append(project_results)

    index_page, data_page = generate_index_html(
        index_template, data_template, results
    )

    if args.out_dir:
        index_path = os.path.join(args.out_dir, 'index.html')
        with open(index_path, 'w') as out_file:
            out_file.write(index_page)

        data_dir = os.path.join(args.out_dir, 'data')

        os.makedirs(data_dir, exist_ok=True)
        with open(os.path.join(data_dir, 'data.js'), 'w') as out_file:
            out_file.write(data_page)


if __name__ == "__main__":
    main()
