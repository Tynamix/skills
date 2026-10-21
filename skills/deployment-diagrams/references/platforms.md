# Platform boundaries and semantics

Use the exact product named in the input. Products in the same row below serve related diagramming roles, not necessarily equivalent capabilities. Verify unfamiliar service placement against current provider documentation.

## Separate containment dimensions

Ownership, geography, network isolation, and orchestration are distinct dimensions. Choose the dimension a view explains; show other dimensions as tags or in another view. A rectangle is a labeled scope, not automatically a firewall.

- **Ownership:** organization, tenant, account, subscription, project, resource group.
- **Location:** region, availability zone, datacenter.
- **Network:** VNet/VPC, subnet, private endpoint, connectivity boundary.
- **Orchestration:** cluster, namespace, controller, workload.

Draw nesting only when it is true for the resources shown. Use tags for overlapping scopes instead of forcing them into a false tree. Label each boundary's kind as well as its name (`Subscription: production`, not just `production`). Containment is shown by nesting, not traffic arrows.

## Azure

- Ownership: Microsoft Entra tenant, management groups, subscriptions, resource groups. Management groups organize subscriptions; resource groups are lifecycle/ownership scopes and can contain resources from multiple regions.
- A VNet is regional; its subnets are not availability-zone boundaries. Show zones on zonal resources or in a separate availability view.
- Distinguish the managed AKS control plane from node pools in the customer's network. Put namespace/workload internals in a logical cluster view when physical placement would otherwise become ambiguous.
- For PaaS private access, draw the **private endpoint NIC inside its subnet** and the target service separately. VNet integration, a private endpoint, and public service access are different connections.
- For landing zones, separate the management-group hierarchy from network topology. Typical identity, management, connectivity, landing-zone, and sandbox subscriptions are roles to confirm, not subscriptions to invent. Show hub/spoke peering and on-premises connectivity only when established by the input.
- Service names commonly needed: Azure Front Door, Application Gateway, API Management, AKS, Container Apps, App Service, Functions, Azure SQL Database, Storage account, Service Bus, Key Vault, Azure Monitor, ExpressRoute.

## AWS

- Ownership: organization, organizational units, accounts. A VPC is regional; a subnet belongs to **one availability zone**. Place multi-AZ deployments in sibling zone/subnet lanes.
- CloudFront, Route 53, IAM, and other global services do not belong inside a regional subnet. Distinguish an S3 bucket's regional placement from VPC placement.
- Managed services have product-specific placement. For example, RDS uses a DB subnet group, while access to S3 through a VPC endpoint does not put the bucket in the VPC.
- Draw the EKS managed control plane separately from customer-managed worker placement. A logical EKS cluster view can include both with their ownership explicitly labeled.
- Identify the actual load balancer type (ALB/NLB) and ingress path. Label internet/NAT gateways, endpoint type, routes, or security groups when relevant; a subnet called `private` alone proves neither isolation nor outbound access.
- A replicated icon does not establish failover. Show primary/standby, active/active, or scaling only when the configuration or proposed design says so.
- Common names: CloudFront, Route 53, Elastic Load Balancing, API Gateway, EC2, ECS, EKS, Lambda, RDS, DynamoDB, S3, SQS, SNS, Secrets Manager, CloudWatch, Direct Connect.

## Google Cloud

- Ownership: organization, folders, projects. A VPC is **global**, a subnet regional, and many compute resources zonal. Never put a whole VPC inside a single zone or imply every service is zonal.
- A Shared VPC has a host project and service projects. Show network ownership separately from workload ownership.
- GKE can be zonal or regional; distinguish the managed control plane from worker pools and check the actual cluster mode. Represent namespaces as logical scopes, not subnets.
- Cloud Storage, Pub/Sub, and other managed APIs are not ordinary VPC-resident VMs. Distinguish Private Google Access, Private Service Connect, and private services access when those paths matter.
- Use the specified load balancer's scope. Global and regional load balancing are different choices.
- Common names: Cloud Load Balancing, Cloud Armor, GKE, Cloud Run, Compute Engine, Cloud SQL, Spanner, Cloud Storage, Pub/Sub, Secret Manager, Cloud Monitoring, Cloud Interconnect.

## Kubernetes, standalone or cloud-hosted

- A cluster contains namespaces; namespaced resources include Deployments, StatefulSets, Services, Ingresses, ConfigMaps, Secrets, PVCs, and Pods. Nodes, PersistentVolumes, and ClusterRoles are cluster-scoped.
- A namespace is not a node pool, subnet, or enforced security boundary by itself. NetworkPolicies need an enforcing implementation; label intended isolation only if supported by the input.
- **Request path:** an external load balancer or ingress/gateway implementation routes to a Service and its selected Pods. Ingress and Gateway API objects configure routing; they are not running proxies themselves. A Service is a logical abstraction, not an extra process.
- **Control relationships:** Deployments/StatefulSets manage Pods; HPAs scale targets. Use a distinct labeled control line, not a request arrow through a Deployment and then a Pod.
- Show replicas as a count or distinct Pods with known placement. Scheduling across zones requires evidence (such as affinity or topology-spread constraints), not just multiple drawn copies.
- A workload claims a PVC; a PVC binds to a cluster-scoped PV, backed by storage. Keep storage ownership and traffic paths distinct.
- Separate logical application views from physical node/pool/zone views when a Pod participates in both. Use the same resource identity in each and mark the repeated depiction.

## Multi-cloud and hybrid

Keep provider boundaries visible. Label both endpoints and the technology of an interconnect: VPN, ExpressRoute, Direct Connect, Cloud Interconnect, public HTTPS, or an explicitly unknown path. Similar labels such as `peering` do not establish cross-provider connectivity.

Place shared identity, delivery, observability, and policy systems in separate lanes from application traffic. Use one shared-system node and labeled control connections rather than replicating it beside every workload. Repeated depictions across views carry the same logical identity and a view reference; they do not imply multiple deployed instances.
