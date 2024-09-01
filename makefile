.PHONY: run stop apply delete build push deploy test render cleanup full-deploy remove-finalizers status

#Run in the background, log everything and register pid
run:
	@python3 src/main_operator.py --verbose > operator.log 2>&1 & echo $$! > pid.txt

#Stop the operator running in the background
stop:
	@if [ -f pid.txt ]; then \
		kill `cat pid.txt`; \
		rm pid.txt; \
		echo "Stopped operator process."; \
	else \
		echo "No operator process running in background."; \
	fi

#Apply the manifests for the functional email resources
apply-good:
	kubectl apply -f examples/example-email-1.yaml -f examples/examples-emailsenderconfig-1.yaml

#Apply the manifests for the non-functional email resources
apply-bad:
	kubectl apply -f examples/example-email-2.yaml -f examples/examples-emailsenderconfig-2.yaml

#Delete the email resources
delete:
	kubectl delete -f examples/example-email-1.yaml -f examples/examples-emailsenderconfig-1.yaml --wait

#Build the docker image
build:
	docker build -t email-operator:latest -f src/Dockerfile src

#Push the docker image to the minikube docker daemon
push:
	minikube image load email-operator:latest

#Package the helm chart
package:
	helm package chart/emailoperator

#Install the helm chart
install:
	helm upgrade --install email-operator ./emailoperator-1.0.0.tgz --namespace default --force --debug

#Full deploy, build the docker image, package the helm chart and install the helm chart
full-deploy: build package install

#Render the helm chart
render:
	helm template email-operator chart/emailoperator --debug

#Remove finalizers from the email resources in order to allow cleanup
remove-finalizers:
	for kind in em esc; do \
		for resource in $$(kubectl get $$kind.teddy.io --no-headers -o custom-columns=":metadata.name"); do \
			kubectl patch $$kind.teddy.io $$resource --type='json' -p='[{"op": "remove", "path": "/metadata/finalizers"}]'; \
		done; \
	done

#Uninstall the helm chart
uninstall-helm:
	helm delete email-operator --namespace default

#Uninstall the CRDs
uninstall-crds:
	kubectl delete crd emails.teddy.io emailsenderconfigs.teddy.io

#Cleanup the helm chart, finalizers and CRDs
cleanup: uninstall-helm remove-finalizers uninstall-crds

#Check the status of the operator, email resources and email sender config resources
status:
	@echo "Checking status of Pods:"
	@kubectl get pods --selector=app=email-operator --namespace default || echo "No operator pods found in the default namespace."
	@echo "\nChecking status of Email resources:"
	@kubectl get em --all-namespaces || echo "No Email resources found."
	@echo "\nChecking status of EmailSenderConfig resources:"
	@kubectl get esc --all-namespaces || echo "No EmailSenderConfig resources found."
	@echo "\nChecking status of CRDs:"
	@kubectl get crd | grep 'teddy.io' || echo "No related CRDs found."
	@echo "\nChecking status of Helm Releases in the default namespace:"
	@helm list --namespace default || echo "No Helm releases found in the default namespace."

