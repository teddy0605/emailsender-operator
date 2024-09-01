import kopf
import kubernetes.client
from kubernetes.client.rest import ApiException
import base64
from email_utils import email_providers
import logging

logger = logging.getLogger(__name__)

@kopf.on.create('teddy.io', 'v1', 'emails')
def create_email(spec, namespace, patch, **kwargs):
    config_ref = spec['senderConfigRef']
    api_client = kubernetes.client.CustomObjectsApi()
    secret_api = kubernetes.client.CoreV1Api()

    try:
        config = api_client.get_namespaced_custom_object(
            group="teddy.io", version="v1", namespace=namespace,
            plural="emailsenderconfigs", name=config_ref)
        secret_ref = config['spec']['apiTokenSecretRef']
        secret = secret_api.read_namespaced_secret(secret_ref, namespace)
        api_token = base64.b64decode(secret.data['apiToken']).decode('utf-8')

        provider_key = config['spec'].get('provider', 'mailersend')
        provider_class = email_providers.get(provider_key)
        if provider_class:
            provider = provider_class(api_token)
            response = provider.send_email(config['spec']['senderEmail'], spec['recipientEmail'], spec['subject'], spec['body'])

            if response and 'status' in response and response['status'] == 'sent':
                patch.status['deliveryStatus'] = 'Success'
                if 'response' in response and isinstance(response['response'], dict) and 'message_id' in response['response']:
                    patch.status['messageId'] = response['response']['message_id']
                else:
                    patch.status['messageId'] = 'N/A'
            else:
                patch.status['deliveryStatus'] = 'Failed'
                if 'message' in response:
                    patch.status['error'] = response['message']
                else:
                    patch.status['error'] = 'Unknown error'
        else:
            logger.error(f"No provider found for {provider_key}")
            patch.status['error'] = 'No provider found'
    except ApiException as e:
        logger.error(f"API error: {e}")
        patch.status['error'] = 'API error occurred'
    except Exception as e:
        logger.error(f"General error: {e}")
        patch.status['error'] = 'Error processing request'


@kopf.on.update('teddy.io', 'v1', 'emails')
def update_email(old, new, name, namespace, logger, **kwargs):
    logger.info(f"Updating Email '{name}' in namespace '{namespace}'.")
    changes = []
    
    for key in ['recipientEmail', 'subject', 'body']:
        old_value = old.get('spec', {}).get(key)
        new_value = new.get('spec', {}).get(key)
        if old_value != new_value:
            changes.append(f"{key}: {old_value} -> {new_value}")
    
    if changes:
        logger.info(f"Changed fields: {', '.join(changes)}")
    else:
        logger.info("No changes detected.")


@kopf.on.delete('teddy.io', 'v1', 'emails')
def delete_email(meta, **kwargs):
    logger.info(f"Email '{meta['name']}' deleted from namespace '{meta['namespace']}'")
