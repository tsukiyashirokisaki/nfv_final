ONOS_IMAGE=onosproject/onos:1.15.0
SSH_KEY=$(cut -d\  -f2 ~/.ssh/id_rsa.pub)
docker start onos-1
docker exec -i onos-$1 /bin/bash -c "cat > config/cluster.json" < config/cluster-$1.json
docker exec -it onos-$1 bin/onos-user-key sdn $SSH_KEY  >/dev/null 2>&1
docker exec -it onos-$1 bin/onos-user-password onos rocks >/dev/null 2>&1

