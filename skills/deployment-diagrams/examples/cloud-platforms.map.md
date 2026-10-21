# cloud-platforms.excalidraw - map

Original illustrative examples, not a discovered or production-ready architecture. Views 1-3 are independent installations; there are no inter-cloud connections. View 4 is a reusable Kubernetes pattern for the Azure and Google Cloud examples, not a shared cluster. AWS uses EC2 instead.

## Views

| View | Prefix | Bounds (x,y,w,h) | Focus |
|------|--------|------------------|-------|
| 1 | `v1-` | 0,0,1280,1328 | azure |
| 2 | `v2-` | 1600,0,1408,1328 | aws |
| 3 | `v3-` | 0,1504,1408,1328 | gcp |
| 4 | `v4-` | 1600,1504,1472,1328 | k8s |

## Resources and boundaries

Each listed ID is a shape; its `-label` and optional `-icon` share its group. Resource group IDs are `g-<element-id>`, nested inside their scope groups. Junctions are drawing notation, not deployed resources.

| Element ID | Parent | Kind | Resource / scope |
|------------|--------|------|------------------|
| `v1-subscription` | `-` | ownership | Subscription: production \| Region: westeurope |
| `v1-vnet` | `v1-subscription` | network | VNet: production (regional) |
| `v1-workers-subnet` | `v1-vnet` | network | Subnet: workers |
| `v1-endpoints-subnet` | `v1-vnet` | network | Subnet: endpoints |
| `v1-aks-workers` | `v1-workers-subnet` | resource | AKS worker pool / Detail: view 4 |
| `v1-sql-endpoint` | `v1-endpoints-subnet` | resource | Private Endpoint / Azure SQL |
| `v1-vault-endpoint` | `v1-endpoints-subnet` | resource | Private Endpoint / Key Vault |
| `v1-sql` | `v1-subscription` | resource | Azure SQL Database |
| `v1-vault` | `v1-subscription` | resource | Azure Key Vault |
| `v2-region` | `-` | ownership | AWS account: production \| Region: eu-west-1 |
| `v2-vpc` | `v2-region` | network | VPC: production (regional) |
| `v2-alb` | `v2-vpc` | resource | Application Load Balancer / public entry |
| `v2-az-a` | `v2-vpc` | location | AZ: eu-west-1a |
| `v2-az-b` | `v2-vpc` | location | AZ: eu-west-1b |
| `v2-subnet-a` | `v2-az-a` | network | Private subnet: a |
| `v2-subnet-b` | `v2-az-b` | network | Private subnet: b |
| `v2-ec2-a` | `v2-subnet-a` | resource | Amazon EC2 / web-a |
| `v2-ec2-b` | `v2-subnet-b` | resource | Amazon EC2 / web-b |
| `v2-rds-primary` | `v2-subnet-a` | resource | Amazon RDS / PostgreSQL primary |
| `v2-rds-standby` | `v2-subnet-b` | resource | Amazon RDS / Multi-AZ standby |
| `v2-sql-junction` | `v2-subnet-a` | junction | Traffic junction (notation, not a deployed resource) |
| `v3-project` | `-` | ownership | Project: production \| Managed services: europe-west1 |
| `v3-vpc` | `v3-project` | network | VPC: app-network (global) |
| `v3-subnet` | `v3-vpc` | network | Subnet: app \| europe-west1 / Private Google Access enabled |
| `v3-gke-workers` | `v3-subnet` | resource | GKE worker pool / Detail: view 4 |
| `v3-psc-endpoint` | `v3-subnet` | resource | Private Service Connect / endpoint |
| `v3-cloud-sql` | `v3-project` | resource | Cloud SQL / PostgreSQL |
| `v3-storage` | `v3-project` | resource | Cloud Storage / regional bucket |
| `v4-cluster` | `-` | logical | Cluster: example \| logical view, not node or zone placement |
| `v4-namespace` | `v4-cluster` | logical | Namespace: orders |
| `v4-deployment` | `v4-namespace` | logical | Deployment: / orders-api (3 Pods) |
| `v4-gateway-proxy` | `v4-cluster` | resource | Gateway proxy / system namespace |
| `v4-service` | `v4-namespace` | resource | Service / orders-api |
| `v4-pod-a` | `v4-deployment` | resource | Pod / orders-api-a |
| `v4-pod-b` | `v4-deployment` | resource | Pod / orders-api-b |
| `v4-pod-c` | `v4-deployment` | resource | Pod / orders-api-c |
| `v4-hpa` | `v4-namespace` | resource | HorizontalPodAutoscaler / orders-api |
| `v4-selector-junction-a` | `v4-namespace` | junction | Traffic junction (notation, not a deployed resource) |
| `v4-selector-junction-b` | `v4-namespace` | junction | Traffic junction (notation, not a deployed resource) |

## Connections

Each ID may have a `-label` overlay. Keep both endpoint bindings and reverse references in sync.

| Arrow ID | From | To | Meaning |
|----------|------|----|---------|
| `v1-workers-to-sql-endpoint` | `v1-aks-workers` | `v1-sql-endpoint` | SQL / TLS |
| `v1-sql-private-link` | `v1-sql-endpoint` | `v1-sql` | private / link |
| `v1-workers-to-vault-endpoint` | `v1-aks-workers` | `v1-vault-endpoint` | secrets / HTTPS |
| `v1-vault-private-link` | `v1-vault-endpoint` | `v1-vault` | private / link |
| `v2-alb-to-a` | `v2-alb` | `v2-ec2-a` | HTTP |
| `v2-alb-to-b` | `v2-alb` | `v2-ec2-b` | HTTP |
| `v2-a-to-sql-junction` | `v2-ec2-a` | `v2-sql-junction` | SQL / TLS |
| `v2-b-to-sql-junction` | `v2-ec2-b` | `v2-sql-junction` | SQL / TLS |
| `v2-junction-to-primary` | `v2-sql-junction` | `v2-rds-primary` | SQL / TLS |
| `v2-primary-to-standby` | `v2-rds-primary` | `v2-rds-standby` | synchronous / replication |
| `v3-workers-to-psc` | `v3-gke-workers` | `v3-psc-endpoint` | SQL / TLS |
| `v3-psc-to-sql` | `v3-psc-endpoint` | `v3-cloud-sql` | PSC / private access |
| `v3-workers-to-storage` | `v3-gke-workers` | `v3-storage` | HTTPS / Private Google Access |
| `v4-proxy-to-service` | `v4-gateway-proxy` | `v4-service` | HTTP |
| `v4-service-to-selector` | `v4-service` | `v4-selector-junction-a` | HTTP / selected Pods |
| `v4-selector-to-a` | `v4-selector-junction-a` | `v4-pod-a` | HTTP |
| `v4-selector-trunk` | `v4-selector-junction-a` | `v4-selector-junction-b` | HTTP |
| `v4-selector-to-b` | `v4-selector-junction-b` | `v4-pod-b` | HTTP |
| `v4-selector-to-c` | `v4-selector-junction-b` | `v4-pod-c` | HTTP |
| `v4-hpa-scales-deployment` | `v4-hpa` | `v4-deployment` | HPA scales Deployment |

## Scope, assumptions, and legend

- Azure: regional VNet with worker and endpoint subnets. Private endpoint NICs are inside the VNet; Azure SQL and Key Vault are outside it. DNS, ingress and the AKS managed control plane are omitted in this selected network view. The worker card points to view 4 without asserting its replica placement.
- AWS: illustrative RDS Multi-AZ DB instance with synchronous standby. Both EC2 instances reach the primary through a drawn SQL-path junction; no client traffic reaches the standby. ALB public subnets in both AZs, routes, security groups and DNS are outside this selected-path scope.
- Google Cloud: a global VPC and regional subnet, with selected GKE worker access through a Private Service Connect endpoint to Cloud SQL, and Private Google Access for Cloud Storage. Managed control plane, DNS and service attachments are omitted. View 4 illustrates the workload pattern.
- Kubernetes: separate system-namespace gateway proxy, namespaced Service, HPA and a Deployment managing three example Pods. Service/branch dots show selection, not extra proxies. Cluster-scoped Nodes and actual zone scheduling are intentionally outside this logical view. Namespace does not itself assert isolation.
- Solid arrows denote requests/private access; the AWS dashed arrow denotes standby replication; the Kubernetes dotted arrow denotes scaling control. Dashed boundaries are networks; dotted boundaries are logical scopes. Dots are intentional traffic junctions; none is a deployed component.
- Abbreviations: AKS = Azure Kubernetes Service; GKE = Google Kubernetes Engine; RDS = Relational Database Service; PSC = Private Service Connect; HPA = HorizontalPodAutoscaler; VPC = virtual private cloud; VNet = virtual network; AZ = availability zone; PaaS = platform as a service.

## Embedded icon provenance

Official SVG bytes retrieved on 2026-10-21 and embedded without modification. SHA-256 identifies each `files` entry. Only icons actually used are included; no external icon requests or local image files are needed.

| File ID (SHA-256) | Product / resource | Official source and usage terms | Package member |
|------------------|--------------------|---------------------------------|----------------|
| `81954a481503057498d543a51863b2eb4673284e109662cdc421051d11dba25c` | Azure Kubernetes Service | [azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) | `Azure_Public_Service_Icons/Icons/containers/10023-icon-service-Kubernetes-Services.svg` |
| `a26124a2b188ccf910520c935c726f7364e0f5935d7a4319ebcab9c80a40e475` | Azure SQL Database | [azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) | `Azure_Public_Service_Icons/Icons/databases/10130-icon-service-SQL-Database.svg` |
| `96de0bb7f0aeb1220d0fd6d337578d5e93dca017d6ea7d42d887aa329b2fd90d` | Azure Private Endpoint | [azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) | `Azure_Public_Service_Icons/Icons/other/02579-icon-service-Private-Endpoints.svg` |
| `712b426f54f0fc50d0816dc79df709daa7ac5f93ccaf4e9b3527f627f6e9ad97` | Azure Key Vault | [azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) | `Azure_Public_Service_Icons/Icons/security/10245-icon-service-Key-Vaults.svg` |
| `27bea44fffd83cc42ce68411e659761a114d41d6b89efc556afef969f96414aa` | Application Load Balancer | [aws](https://aws.amazon.com/architecture/icons/) | `Resource-Icons_07312026/Res_Networking-Content-Delivery/Res_Elastic-Load-Balancing_Application-Load-Balancer_48.svg` |
| `099dff32b3f795f3fa8ed97f0466708502a7fd6500136679899a0cec5a5a2473` | Amazon EC2 | [aws](https://aws.amazon.com/architecture/icons/) | `Architecture-Service-Icons_07312026/Arch_Compute/48/Arch_Amazon-EC2_48.svg` |
| `5ef651fae418df2ceade6bf9cbf779d8c8f2ec35c6ff47b23934b10722b6790e` | Amazon RDS | [aws](https://aws.amazon.com/architecture/icons/) | `Architecture-Service-Icons_07312026/Arch_Databases/48/Arch_Amazon-RDS_48.svg` |
| `6a33654c499bc4c38012661875a1a8c1bf2cdf01be8fdcc90d1c6504657878ec` | Google Kubernetes Engine | [gcp](https://cloud.google.com/icons) | `Unique Icons/GKE/SVG/GKE-512-color.svg` |
| `4e0d3d2049a67f64e5a2c88f836bf2d1786f809a72d82279b18906ec9d6b35c9` | Cloud SQL | [gcp](https://cloud.google.com/icons) | `Unique Icons/Cloud SQL/SVG/CloudSQL-512-color.svg` |
| `df42fc4b652cb133a4150bea7988aa965651d2c52fdfd141b6e8a359552eec8e` | Cloud Storage | [gcp](https://cloud.google.com/icons) | `Unique Icons/Cloud Storage/SVG/Cloud_Storage-512-color.svg` |
| `3356f7ca970f811da2b1aa34a0f13e846255378727809ab6629837a842db0a2d` | Pod | [k8s](https://github.com/kubernetes/community/tree/main/icons) | `icons/svg/resources/unlabeled/pod.svg` |
| `a86fad881253c4d7abbe7413c0efbca2e7dde7e54a55774f79349494bd823990` | Service | [k8s](https://github.com/kubernetes/community/tree/main/icons) | `icons/svg/resources/unlabeled/svc.svg` |
| `d96f6e93a0f57ca9583b2120e3ddb4453afb5a29aa6d8c1360e8eb8e458489f7` | Deployment | [k8s](https://github.com/kubernetes/community/tree/main/icons) | `icons/svg/resources/unlabeled/deploy.svg` |
| `7b92a11ab6050825927bc91bf654499a02e8f8488b059d2578ab22037900fbed` | HorizontalPodAutoscaler | [k8s](https://github.com/kubernetes/community/tree/main/icons) | `icons/svg/resources/unlabeled/hpa.svg` |

Azure artwork is used under Microsoft's permission for architectural diagrams on the linked source page. AWS artwork is used under the architecture toolkit permission on its source page. Google Cloud artwork comes from the official library provided for diagrams and technical documentation.

Kubernetes resource icons: Kubernetes community contributors, unchanged, used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as offered by the [icon-set license](https://github.com/kubernetes/community/tree/main/icons#license). The Kubernetes logo is a Linux Foundation trademark; [trademark guidelines](https://www.linuxfoundation.org/trademark-usage/) apply. This example does not imply endorsement by any provider.

Fallback: `v3-psc-endpoint` is a native labeled card because the retrieved Google Cloud core-product package has no exact Private Service Connect icon. The generic gateway proxy and traffic junctions are intentionally native notation, not provider-icon substitutes.

## Validation

- Structural checks passed: 146 elements, 20 resource cards, 20 bound arrows, four views, and 14 unique embedded SVGs. IDs, forward/reverse bindings, containment, icon hashes/aspect ratios, route clearance from unrelated cards, and local documentation links were checked.
- Imported and rendered locally with Excalidraw 0.18.1. All elements survived restoration, all 14 SVGs decoded, and all 20 arrows retained both endpoint bindings. All four rendered views were visually inspected.
- Measured all 68 text boxes (97 lines) with Helvetica metrics. Every line fits with the documented 16px allowance; no label ink intersects an arrow segment or rectangle outline.
- In a disposable editor copy, moved the AKS resource group 100px using the editor's keyboard action. Card, icon, and label moved together; both attached arrow endpoints followed and remained adjacent to the card. Exported that copy as Excalidraw JSON and reimported it: all 146 IDs, 20 arrow bindings, 14 image records, and the resource grouping survived.
- The delivered layout was not changed by the movement test. Explicit polyline bends can require rerouting after a move; this is not an automatic obstacle router. Other editor versions were not tested.
