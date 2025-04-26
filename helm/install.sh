#!/usr/bin/env bash
my_dir=$(dirname $(realpath $0))

kubectl create ns meta
kubectl create ns notes-app
helm repo add grafana https://grafana.github.io/helm-charts && helm repo update
helm install --values $my_dir/loki-values.yml loki grafana/loki -n meta
helm install --values $my_dir/grafana-values.yml grafana grafana/grafana --namespace meta
helm install --values $my_dir/k8s-monitoring-values.yml k8s grafana/k8s-monitoring -n meta