#
# Copyright (c) 2015-2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import trustedanalytics as ta

from common import AtkTestException, parse_arguments, check_uaa_file

parameters = parse_arguments()

ta.create_credentials_file(parameters.uaa_file_name)

check_uaa_file(parameters.uaa_file_name)

query = "select * from " + parameters.database_name + "." + parameters.table_name
print("\nQuery: {}".format(query))
hq = ta.HiveQuery(query)
frame = ta.Frame(hq)
