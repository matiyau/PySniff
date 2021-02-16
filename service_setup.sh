DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sudo mkdir -p /usr/lib/iot_proj1/code
sudo cp -R "$DIR"/* /usr/lib/iot_proj1/code

sudo cp "$DIR"/iot_proj1.service /lib/systemd/system/

sudo systemctl enable iot_proj1.service
sudo systemctl start iot_proj1.service