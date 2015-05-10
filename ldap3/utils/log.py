"""
"""

# Created on 2015.05.01
#
# Author: Giovanni Cannata
#
# Copyright 2015 Giovanni Cannata
#
# This file is part of ldap3.
#
# ldap3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ldap3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ldap3 in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

from logging import getLogger, getLevelName, DEBUG

# logging
VERBOSITY_NONE = 0
VERBOSITY_ERROR = 10
VERBOSITY_BASIC = 20
VERBOSITY_PROTOCOL = 30
VERBOSITY_NETWORK = 40

VERBOSITY_LEVELS = [VERBOSITY_NONE,
                    VERBOSITY_ERROR,
                    VERBOSITY_BASIC,
                    VERBOSITY_PROTOCOL,
                    VERBOSITY_NETWORK]
LIBRARY_VERBOSITY_LEVEL = VERBOSITY_NONE
LIBRARY_LOGGING_LEVEL = DEBUG

logging_level = None
verbosity_level = None
logging_encoding = 'ascii'

try:
    from logging import NullHandler
except ImportError:  # NullHandler not present in Python < 2.7
    from logging import Handler

    class NullHandler(Handler):
        def handle(self, record):
            pass

        def emit(self, record):
            pass

        def createLock(self):
            self.lock = None


def get_verbosity_level_name(level):

    if level == VERBOSITY_NONE:
        return 'NONE'
    elif level == VERBOSITY_ERROR:
        return 'ERROR'
    elif level == VERBOSITY_BASIC:
        return 'BASIC'
    elif level == VERBOSITY_PROTOCOL:
        return 'PROTOCOL'
    elif level == VERBOSITY_NETWORK:
        return 'NETWORK'
    raise ValueError('unknown verbosity level')


def log(verbosity, message, *args):
    if verbosity <= verbosity_level:
        encoded_message = (get_verbosity_level_name(verbosity) + ':' + message % args).encode(logging_encoding, 'backslashreplace')
        logger.log(logging_level, encoded_message)


def log_enabled(verbosity):
    if verbosity <= verbosity_level:
        if logger.isEnabledFor(logging_level):
            return True

    return False


def set_library_log_activation_level(level):
    if isinstance(level, int):
        global logging_level
        logging_level = level
    else:
        if log_enabled(VERBOSITY_ERROR):
            log(VERBOSITY_ERROR, 'invalid library log activation level <%s> ', level)
        raise ValueError('invalid library log activation level')


def set_library_verbosity_level(verbosity):
    if verbosity in VERBOSITY_LEVELS:
        global verbosity_level
        verbosity_level = verbosity
        if log_enabled(VERBOSITY_ERROR):
            log(VERBOSITY_ERROR, 'verbosity level set to ' + get_verbosity_level_name(verbosity_level))
    else:
        if log_enabled(VERBOSITY_ERROR):
            log(VERBOSITY_ERROR, 'unable to set verbosity level to <%s>', verbosity)
        raise ValueError('invalid library verbosity level')

# set a logger for the library with NullHandler. It can be used by the application with its own logging configuration
logger = getLogger('ldap3')
logger.addHandler(NullHandler())
set_library_log_activation_level(LIBRARY_LOGGING_LEVEL)
set_library_verbosity_level(LIBRARY_VERBOSITY_LEVEL)

# emits a info message to let the application know that ldap3 logging is available when the log level is set to logging_level
logger.info('ldap3 library initialized - logging emitted with loglevel set to ' + getLevelName(logging_level) + ' - available verbosity levels are: ' + ', '.join([get_verbosity_level_name(level) for level in VERBOSITY_LEVELS]))