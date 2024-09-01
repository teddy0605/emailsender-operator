import kopf
import logging
import email_handler
import emailsenderconfig_handler

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    kopf.run()

