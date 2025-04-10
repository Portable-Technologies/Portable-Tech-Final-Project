
# Configuring EKS Cluster via Cloud9

## Configure your permanent credentials and disable Cloud9 temporary credentials
`/usr/local/bin/aws cloud9 update-environment --environment-id $C9_PID --managed-credentials-action DISABLE`

## Clear current credentials file
`> -vf ${HOME}/.aws/credentials`

## Use credentials from AWS Academy AWS Details and copy them into ~/.aws/credentials file
`vi ~/.aws/credentials` 

### IMPORTANT: Double-check and make sure it looks ok. It needs to start with [default] line and then 3 lines with aws_access_key_id, aws_secret_access_key, aws_session_token
`cat ~/.aws/credentials `

`sudo yum -y install jq gettext bash-completion`

## Install eksctl
`curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp`
`sudo mv -v /tmp/eksctl /usr/local/bin`

## Create EKS Cluster
`eksctl create cluster -f eks_config.yaml`

## Install kubectl 
```
curl -LO https://dl.k8s.io/release/v1.29.13/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/
alias k='kubectl'
```

`cat eks_config.yaml | grep ARN`
