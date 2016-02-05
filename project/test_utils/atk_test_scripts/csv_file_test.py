##############################################################################
# INTEL CONFIDENTIAL
#
# Copyright 2015 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code (Material) are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material may contain trade secrets and
# proprietary and confidential information of Intel Corporation and its
# suppliers and licensors, and is protected by worldwide copyright and trade
# secret laws and treaty provisions. No part of the Material may be used,
# copied, reproduced, modified, published, uploaded, posted, transmitted,
# distributed, or disclosed in any way without Intel's prior express written
# permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or
# delivery of the Materials, either expressly, by implication, inducement,
# estoppel or otherwise. Any license under such intellectual property rights
# must be express and approved by Intel in writing.
##############################################################################

import datetime
import os

import trustedanalytics as ta

from common import AtkTestException, parse_arguments, check_uaa_file


parameters = parse_arguments()

directory = os.path.dirname(__file__)

ta.create_credentials_file(parameters.uaa_file_name)

check_uaa_file(parameters.uaa_file_name)

hdfs_path = parameters.target_uri.split("/", 3)[3]
print("calling CsvFile...")
hcsv = ta.CsvFile("../../../" + hdfs_path, schema=[('line' + str(i), str) for i in xrange(8)], delimiter=",")
frame = ta.Frame(hcsv)

frame_content = frame.inspect(20)
print("original_table_content: ", frame_content)
frame_rows = frame_content.rows

if frame.row_count == 17:
    print("Frame of file {} created correctly".format(hdfs_path))
else:
    raise AtkTestException("Frame of file {} not created correctly".format(hdfs_path))
