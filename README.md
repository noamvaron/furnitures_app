
## Overview

This application uses several services deployed in different namespaces in a Kubernetes cluster. The following guide provides instructions for port-forwarding these services using ⁠ kubectl ⁠.

## Port-Forwarding Services

Port-forwarding allows you to access your services locally as if they were running on your machine. Below are the commands to port-forward various services in your Kubernetes cluster.

### Argo CD Server

Namespace: ⁠ argocd ⁠

Command:
⁠ sh
kubectl port-forward svc/argocd-server -n argocd 8080:443
 ⁠
password: bKr7FoL0vtj3VcMs

### Jenkins

Namespace: ⁠ jenkins ⁠

Command:
⁠ sh
kubectl port-forward svc/jenkins -n jenkins 8081:8080

password: UQTqL6wrWXUhPDk1Y5mLYh
 ⁠

### Prometheus

Namespace: ⁠ monitoring ⁠

Command:
⁠ sh
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
 ⁠

### Grafana

Namespace: ⁠ monitoring ⁠

Command:
⁠ sh
kubectl port-forward svc/prometheus-grafana -n monitoring 3000:3000
 ⁠
password: prom-operator

### My Application

Namespace: ⁠ default ⁠

Command:
⁠ sh
kubectl port-forward svc/furnitures-app-myapp -n default 5000:5000
 ⁠
