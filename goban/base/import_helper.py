# Copyright (C) 2016 Goban authors
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import importlib

def import_helper(name):
    module_name, class_name = name.rsplit('.', 1)
    print module_name, class_name
    return getattr(importlib.import_module(module_name), class_name)
