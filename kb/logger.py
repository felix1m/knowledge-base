# -*- coding: utf-8 -*-
"""
    kb.logger
    ~~~~~~~~~~~~~~~~

    kb logger module
"""

import logging
import logging.handlers

from logging.handlers import SMTPHandler, TimedRotatingFileHandler
LOG_FILENAME = 'testing.log'
LOG_MAX_BYTES = 2000
LOG_MAX_BACKUP = 100


BUG_MAIL_SENDER = 'bugs@kb.com'
BUG_MAIL_SERVER = 'smtp.gmail.com'
BUG_MAIL_RECEIVERS = ['api-errors@kb.flowdock.com']
BUG_MAIL_PORT = 587
BUG_MAIL_USERNAME = 'info@kb.com'
BUG_MAIL_PASSWORD = 'ukjJTBYz'


class TlsSMTPHandler(SMTPHandler):
    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            import string # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.ehlo() # for tls add this line
                smtp.starttls() # for tls add this line
                smtp.ehlo() # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def setup_logging(app):
    mh = TlsSMTPHandler((BUG_MAIL_SERVER, BUG_MAIL_PORT), BUG_MAIL_SENDER, BUG_MAIL_RECEIVERS, 'Error found!', (BUG_MAIL_USERNAME, BUG_MAIL_PASSWORD))
    mh.setLevel(logging.ERROR)

    def namer(name):
        return name + ".gz"

    def rotator(source, dest):
        with open(source, "rb") as sf:
            data = sf.read()
            compressed = zlib.compress(data, 9)
            with open(dest, "wb") as df:
                df.write(compressed)
        os.remove(source)

    rh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=LOG_MAX_BYTES, backupCount=LOG_MAX_BACKUP)
    mh.setLevel(logging.WARNING)
    rh.rotator = rotator
    rh.namer = namer

    loggers = [logging.getLogger()]
    # loggers = [app.logger, logging.getLogger('sqlalchemy')]
    for logger in loggers:
        logger.addHandler(rh)
        logger.addHandler(mh)
