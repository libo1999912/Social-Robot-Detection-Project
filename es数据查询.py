from elasticsearch import Elasticsearch
import json
import ssl
host = ['https://10.161.22.32:9210','https://10.161.22.33:9210','https://10.161.22.34:9210','https://10.161.22.35:9210','https://10.161.22.36:9210']
username = 'elastic-robot'
password = 'Golaxy@123'
ca_certs = '/etc/pki/ca-trust/source/anchors/http_ca.crt'

es = Elasticsearch(hosts=host,
                   request_timeout=1000,
                   basic_auth=(username,password),
                   ca_certs = ca_certs,
                   verify_certs=False)
# 查询体
search_query ={
"size": 100000,
"query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "media_name": "快手短视频"
                    }
                },
                {
                    "terms": {
                        "msg_type": [
                            "11",
                            "12"
                        ]
                    }
                }
            ]
        }
    }
}


search_query["track_total_hits"] = True
search = es.search(index="base_data-2023.05.22", body=search_query)
with open("ks_content_0522_10W_charushijian.json","w", encoding="utf-8") as f:
    json.dump(search["hits"]["hits"],f,ensure_ascii = False)

es.close()
