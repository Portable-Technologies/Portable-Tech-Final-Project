## Folder Structure
```
Portable-Tech-Final-Project/
│
├── cluster/                      # eksctl cluster config and notes
│   └── eks_config.yaml
│
├── k8s-manifests/               # All Kubernetes YAML definitions
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── pvc.yaml
│   ├── rbac.yaml
│   ├── mysql.yaml
│   └── flask.yaml
│
├── templates/                   # HTML templates for the Flask app
│   └── index.html               # (or any other Jinja templates)
│
├── Dockerfile                   # For Flask app
├── Dockerfile_mysql             # Optional, if custom MySQL config needed
├── app.py                       # Your main Flask app
├── mysql.sql                    # DB schema for initializing MySQL
└── requirements.txt             # Python dependencies

```



## Configuring EKS Cluster via Cloud9

### - Configure your permanent credentials and disable Cloud9 temporary credentials
`/usr/local/bin/aws cloud9 update-environment --environment-id $C9_PID --managed-credentials-action DISABLE`

### - Clear current credentials file
`> -vf ${HOME}/.aws/credentials`

### - Use credentials from AWS Academy AWS Details and copy them into ~/.aws/credentials file
`vi ~/.aws/credentials` 

### - IMPORTANT: Double-check and make sure it looks ok. It needs to start with [default] line and then 3 lines with aws_access_key_id, aws_secret_access_key, aws_session_token
`cat ~/.aws/credentials `

`sudo yum -y install jq gettext bash-completion`

### - Install eksctl
`curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp`
`sudo mv -v /tmp/eksctl /usr/local/bin`

### - Create EKS Cluster
update eks_config.yaml
`cat eks_config.yaml | grep ARN`
`eksctl create cluster -f eks_config.yaml`

### - Install kubectl 
```
curl -LO https://dl.k8s.io/release/v1.29.13/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/
alias k='kubectl'
```

### - Install The Amazon EBS CSI driver 
`kubectl apply -k 'github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.32'`

