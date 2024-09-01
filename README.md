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

- Kubernetes cluster
- Helm 3
- Docker

## Installation

### Using Helm

1. Clone the repository:
   ```
   git clone https://github.com/teddy0605/emailsender-operator.git
   cd email-operator
   ```

2. Install the Helm chart:
   ```
   helm install email-operator ./chart/emailsender-operator
   ```

### Manual Installation

1. Build the Docker image:
   ```
   make build
   ```

2. Push the image to your registry:
   ```
   make push
   ```

3. Deploy the operator:
   ```
   make install
   ```

## Usage

1. Create an `EmailSenderConfig` resource:
    ```
    yaml
    apiVersion: teddy.io/v1
    kind: EmailSenderConfig
    metadata:
    name: my-email-config
    spec:
    apiTokenSecretRef: my-email-secret
    senderEmail: sender@example.com
    ```

2. Create an `Email` resource:
    ```
    yaml
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

Refer to the `values.yaml` file in the Helm chart for configurable parameters.

## Development

To run the operator locally for development:

```
make run
```

To stop the local development process:

```
make stop
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
