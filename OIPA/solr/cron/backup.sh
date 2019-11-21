#!/bin/sh
rm -rf /var/solr/data/$1/data/snapshot.$1
curl --url "http://localhost:8983/solr/$1/replication?command=backup&name=$1"