
#Light 1
curl -s --request POST "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU HTTP/1.1" \
--data '{"method":"passthrough", "params": {"deviceId": "8012CFBDD636A8E1C9B2248B3850543B19C8665F", "requestData": "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"ignore_default\":1, \"on_off\":1, \"color_temp\":3800, \"brightness\":80}}}" }}' \
--header "Content-Type: application/json"

#Light 2
curl -s --request POST "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU HTTP/1.1" \
--data '{"method":"passthrough", "params": {"deviceId": "8012B569B7255CD98542E8D6F1F308A319C7ACC6", "requestData": "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"ignore_default\":1, \"on_off\":1, \"color_temp\":3800, \"brightness\":80}}}" }}' \
--header "Content-Type: application/json"

#Light 3
curl -s --request POST "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU HTTP/1.1" \
--data '{"method":"passthrough", "params": {"deviceId": "80121EE053655BB04B5D29A83226E69E19C65783", "requestData": "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"ignore_default\":1, \"on_off\":1, \"color_temp\":3800, \"brightness\":80}}}" }}' \
--header "Content-Type: application/json"

