# Email Operator for Kubernetes

## Overview

The Email Operator for Kubernetes is a custom controller that manages email sending operations within a Kubernetes cluster. It utilizes the Kopf framework and integrates with email service providers like Mailersend to facilitate email dispatch directly from Kubernetes resources.

## Features

- Custom Resource Definitions (CRDs) for `Email` and `EmailSenderConfig`
- Secure management of email provider credentials using Kubernetes Secrets
- Extensible architecture supporting multiple email service providers
- Full lifecycle management of email resources
- Event logging and status updates for email operations

## Prerequisites

- Kubernetes cluster (tested with v1.24+)
- Helm 3
- Docker
- Python 3.9+
- MailerSend account and API token

## Setting up MailerSend

1. Create a MailerSend account at https://mailersend.com
2. Generate an API token from the MailerSend dashboard:
   - Go to Settings → API Tokens
   - Click "Create New Token"
   - Give it a name and ensure it has "Email Send" permission
   - Copy the generated token

3. Base64 encode your API token:
   ```bash
   echo -n "your-api-token-here" | base64
   ```

4. Update the `values.yaml` with your encoded token:
   ```yaml
   providers:
     - name: mailersend
       apiToken: <your-base64-encoded-token>
       senderEmail: your-verified-sender@domain.com
   ```

   Note: Make sure your sender email is verified in MailerSend dashboard.

## Installation

### Using Helm

1. Clone the repository:
   ```bash
   git clone https://github.com/teddy0605/emailsender-operator.git
   cd email-operator
   ```

2. Configure your email provider credentials in `values.yaml`

3. Install the Helm chart:
   ```bash
   helm install email-operator ./chart/emailsender-operator
   ```

### Manual Installation

1. Build the Docker image:
   ```bash
   make build
   ```

2. Push the image to your registry:
   ```bash
   make push
   ```

3. Deploy the operator:
   ```bash
   make install
   ```

## Usage

1. Create an `EmailSenderConfig` resource:
    ```yaml
    apiVersion: teddy.io/v1
    kind: EmailSenderConfig
    metadata:
      name: my-email-config
    spec:
      apiTokenSecretRef: my-email-secret
      senderEmail: sender@example.com
    ```

2. Create an `Email` resource:
    ```yaml
    apiVersion: teddy.io/v1
    kind: Email
    metadata:
      name: test-email
    spec:
      senderConfigRef: my-email-config
      recipientEmail: recipient@example.com
      subject: "Test Email"
      body: "This is a test email sent via the Kubernetes Email Operator."
    ```

## Configuration

Refer to the `values.yaml` file in the Helm chart for configurable parameters. Key parameters include:

- `image.repository`: Docker image repository
- `image.tag`: Docker image tag
- `resources`: CPU/Memory resource requests and limits
- `providers`: Email provider configurations

## Development

To run the operator locally for development:

```bash
make run
```

To stop the local development process:

```bash
make stop
```

## Roadmap / TODO

Future improvements planned for this project:

1. **Observability**
   - [ ] Add Prometheus metrics for monitoring email operations
   - [ ] Implement health check endpoints
   - [ ] Enhanced logging and tracing

2. **Reliability**
   - [ ] Add rate limiting for email sending
   - [ ] Implement retry mechanism with exponential backoff
   - [ ] Add circuit breaker for provider failures

3. **Security**
   - [ ] Implement proper API token rotation
   - [ ] Add support for multiple authentication methods
   - [ ] Enhanced secret management

4. **Features**
   - [ ] Support for HTML emails
   - [ ] Email templates
   - [ ] Attachment support
   - [ ] Multiple recipient support

5. **Testing**
   - [ ] Add unit tests
   - [ ] Add integration tests
   - [ ] Add E2E tests

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue on GitHub.
