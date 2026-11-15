#!/bin/bash
# delete the Photo Notes VPC and everything in it, in dependency order
q() { aws ec2 "$@" --output text; }
V=$(q describe-vpcs --filters Name=tag:Name,Values=photo-notes-vpc --query 'Vpcs[0].VpcId')
F="Name=vpc-id,Values=$V"
I=$(q describe-instances --filters $F Name=instance-state-name,Values=pending,running,stopped \
    --query 'Reservations[].Instances[].InstanceId')
[ -n "$I" ] && q terminate-instances --instance-ids $I >/dev/null \
    && aws ec2 wait instance-terminated --instance-ids $I
N=$(q describe-nat-gateways --filter $F Name=state,Values=pending,available \
    --query 'NatGateways[].NatGatewayId')
for n in $N; do q delete-nat-gateway --nat-gateway-id $n >/dev/null; done
[ -n "$N" ] && aws ec2 wait nat-gateway-deleted --nat-gateway-ids $N
for e in $(q describe-vpc-endpoints --filters $F --query 'VpcEndpoints[].VpcEndpointId'); do
  q delete-vpc-endpoints --vpc-endpoint-ids $e >/dev/null
done
left() { q describe-vpc-endpoints --filters $F --query 'VpcEndpoints[].VpcEndpointId'; }
while [ -n "$(left)" ]; do sleep 5; done
for g in $(q describe-security-groups --filters $F \
    --query "SecurityGroups[?GroupName!='default'].GroupId"); do
  q delete-security-group --group-id $g
done
for s in $(q describe-subnets --filters $F --query 'Subnets[].SubnetId'); do
  q delete-subnet --subnet-id $s
done
for r in $(q describe-route-tables --filters $F \
    --query 'RouteTables[?Associations[0].Main != `true`].RouteTableId'); do
  q delete-route-table --route-table-id $r
done
for a in $(q describe-network-acls --filters $F Name=default,Values=false \
    --query 'NetworkAcls[].NetworkAclId'); do
  q delete-network-acl --network-acl-id $a
done
for i in $(q describe-internet-gateways --filters Name=attachment.vpc-id,Values=$V \
    --query 'InternetGateways[].InternetGatewayId'); do
  q detach-internet-gateway --internet-gateway-id $i --vpc-id $V
  q delete-internet-gateway --internet-gateway-id $i
done
q delete-vpc --vpc-id $V && echo "deleted $V"
