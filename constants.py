# -*- coding: utf-8 -*-

import sys, os

is_py3 = sys.version_info[0] == 3

if is_py3:
    from configparser import ConfigParser as configuration_parser
else:
    from ConfigParser import SafeConfigParser as configuration_parser


CONFIG = configuration_parser()
CONFIG.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))
POP_UP_TIMEOUT = int(CONFIG.get('general', 'pop_up_timeout'))
PROMPT_TIMEOUT = int(CONFIG.get('general', 'prompt_timeout'))
ALWAYS_ON_TOP = bool(CONFIG.get('general', 'always_on_top'))
SANITIZATION_LEVEL = CONFIG.get('general', 'sanitization_level')
GREEKENGLISH_CONVERSION = CONFIG.get('general', 'replace_english_with_greek')
