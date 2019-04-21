Information
---

##### Description
 - Webhook of Grafana for teamplus messager
 
##### Run service
 - python3 guardain-grafana.py


Configure File
---

##### file name
 - guardian.conf

##### [Teamplus]
 
 - api_url - TeamPlus API URL
 - account - TeamPlus 帳號名稱
 - api_key - TeamPlus 帳號的API Key
 - chat_sn - TeamPlus 聊天室編號

 
##### [GrafanaWebhook]

 - api_port - 服務Port
 - prefix - 推播teamplus訊息的前綴

