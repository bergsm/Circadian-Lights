
#curl -s --request POST "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU HTTP/1.1" \
#--data '{"method":"passthrough", "params": {"deviceId": "8012CFBDD636A8E1C9B2248B3850543B19C8665F", "requestData": "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"color_temp\":6500}}}" }}' \
#--header "Content-Type: application/json"

curl -s --request POST "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU HTTP/1.1" \
--data '{"method":"passthrough", "params": {"deviceId": "8012CFBDD636A8E1C9B2248B3850543B19C8665F", "requestData": "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"ignore_default\":1, \"on_off\":1, \"color_temp\":3300, \"brightness\":80}}}" }}' \
--header "Content-Type: application/json"
