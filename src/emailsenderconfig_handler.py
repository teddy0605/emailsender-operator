import kopf
import logging

logger = logging.getLogger(__name__)

@kopf.on.create('teddy.io', 'v1', 'emailsenderconfigs')
def create_emailsenderconfig(spec, name, namespace, logger, **kwargs):
    logger.info(f"Creating EmailSenderConfig '{name}' in namespace '{namespace}' with senderEmail: {spec.get('senderEmail', 'Not provided')}")
    if 'senderEmail' not in spec:
        message = "EmailSenderConfig must include 'senderEmail'."
        logger.error(message)
        raise kopf.PermanentError(message)

@kopf.on.update('teddy.io', 'v1', 'emailsenderconfigs')
def update_emailsenderconfig(spec, old, new, name, namespace, logger, **kwargs):
    logger.info(f"Updating EmailSenderConfig '{name}' in namespace '{namespace}'.")
    changes = []

    for key in spec.keys():
        old_value = old.get('spec', {}).get(key)
        new_value = new.get('spec', {}).get(key)
        if old_value != new_value:
            changes.append(f"{key}: {old_value} -> {new_value}")
    
    if changes:
        logger.info(f"Changed fields: {', '.join(changes)}")
    else:
        logger.info("No changes detected.")

@kopf.on.delete('teddy.io', 'v1', 'emailsenderconfigs')
def delete_emailsenderconfig(meta, logger, **kwargs):
    logger.info(f"Deleting EmailSenderConfig '{meta['name']}' from namespace '{meta['namespace']}'")


