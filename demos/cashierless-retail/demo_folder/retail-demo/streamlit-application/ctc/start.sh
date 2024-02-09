#!/bin/bash

export DOMAIN_NAME="${DOMAIN_NAME:-$(kubectl get -n ezapp-system cm ezapp-ezua-envs-cm -o jsonpath='{.data.DOMAIN_NAME}')}"
export ENDPOINT="end2end.${DOMAIN_NAME}"

APP_LOGO=$(base64 logo.jpg | tr -d '\n' 2> /dev/null)
export APP_LOGO

#Added to be consistent with other apps
if [ -z "$AIRGAP_REGISTRY_URL" ]; then
  kubectl -n ezua-system get configmap ezua-cluster-config > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    AIRGAP_REGISTRY_URL=$(kubectl get cm -n ezua-system ezua-cluster-config -o jsonpath="{.data.airgap\.registryUrl}")
    export AIRGAP_REGISTRY_URL
  else
      echo "WARNING: Kubeflow: ezua-system/ezua-cluster-config CM not found"
  fi
fi

yq '
  .ezua.domainName = strenv(DOMAIN_NAME) |
  .ezua.virtualService.endpoint = strenv(ENDPOINT) |
  .airgap.registry = strenv(AIRGAP_REGISTRY_URL) |
  del(.ezua.authorizationPolicy) |
  del(.ezua.virtualService.istioGateway) |
  del(.installer)' chart/values.yaml > tmp.yaml

IFS= read -rd '' output < <(cat tmp.yaml)
output=$output yq -iP e '.spec.values = strenv(output)' end2end-ezappconfig.yaml
rm tmp.yaml

yq -i e '.spec.logoImage = strenv(APP_LOGO)' end2end-ezappconfig.yaml

# If deployed on openshift cluster, create network attachment defination in kubeflow namespace
if [[ ${DEPLOY_TARGET} == "byok" ]] && [[ ${DEPLOY_ENV} == "openshift" ]]; then
  # Create namespace if not available
  END2END_NAMESPACE="end2end"
  kubectl get ns ${END2END_NAMESPACE} > /dev/null 2>&1
  if [[ $? -ne 0 ]]; then
    echo "${END2END_NAMESPACE}: ${END2END_NAMESPACE} namespace does not exist; creating..."
    kubectl create ns ${END2END_NAMESPACE}
    if [[ $? -ne 0 ]]; then
      echo "${END2END_NAMESPACE}: ERROR: Could not create ${END2END_NAMESPACE} namespace" && exit 1
    fi
  else
    echo "${END2END_NAMESPACE}: ${END2END_NAMESPACE} namespace already exists"
  fi
  kubectl apply -f ../net-attach-def.yaml -n ${END2END_NAMESPACE}
  if [[ $? -ne 0 ]]; then
    echo "ERROR: Could not create network attachment defination in ${END2END_NAMESPACE} namespace" && exit 1
  fi
fi

kubectl apply -f end2end-ezappconfig.yaml