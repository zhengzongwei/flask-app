#  Copyright (c)2024. zhengzongwei
#  flask-app-backend is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
#  EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
#  MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.

import logging
import os
from logging.handlers import TimedRotatingFileHandler

import toml

LOG_LEVEL_MAPPING = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL
}


class LogConfigError(Exception):
    message = "Error loading logging configuration: %(log_config)s: %(message)s"

    def __init__(self, log_config, message):
        self.log_config = log_config
        self.err_msg = message

    def __str__(self):
        return self.message % dict(log_config=self.log_config, message=self.err_msg)


class Logger(object):
    default_log_config = {
        "level": "debug",
        "log_dir": "",
        "log_file": "",
        # "log_format": "%(asctime)s - %(name)s[func: %(funcName)s line:%(lineno)d] - %(levelname)s: %(message)s",
        "log_format": "%(asctime)s %(process)d %(levelname)s %(name)s %(message)s [%(funcName)s] %("
                      "pathname)s:%(lineno)d]",
        "log_console": True

    }

    def __init__(self, logger_name=None, logger_conf_path=None):
        self.logger_name = logger_name
        self.logger_conf_path = logger_conf_path
        self.logger_conf = self.default_log_config

        self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger(self.logger_name)
        if self.logger_conf_path is not None:
            self._get_log_config()

        self.logger.setLevel(LOG_LEVEL_MAPPING[self.logger_conf.get("level", "INFO").upper()])

        # 如果是debug模式 或者开启了 log_console 则打印日志在console
        if not self.logger_conf.get("log_console", False) or self.logger_conf.get("level").lower() == "debug":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(self.logger_conf.get("log_format")))
            self.logger.addHandler(console_handler)

        if self.logger_conf_path is not None:
            log_path = self._get_log_file_path()
            file_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1, backupCount=3,
                                                    encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(self.logger_conf.get("log_format")))
            self.logger.addHandler(file_handler)

    def _get_log_config(self):
        try:
            log_conf = toml.load(self.logger_conf_path)
            self.logger_conf = log_conf.get('logs', {})
        except LogConfigError as e:
            logging.warning("No logging configuration,Use default logging configuration!")
        return self.logger_conf

    def _get_log_file_path(self):
        log_dir = self.logger_conf.get("log_dir")
        log_file = self.logger_conf.get("log_file")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if log_dir and log_file:
            return os.path.join(log_dir, log_file)
        if log_file and not log_dir:
            return log_file
        if log_dir:
            return '%s.log' % os.path.join(log_dir, self.logger_name)

        return None

    def getLogger(self):
        return self.logger
