DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sudo mkdir -p /usr/lib/pysniff
sudo cp -R "$DIR"/../pysniff /usr/lib/pysniff
sudo cp -R "$DIR"/../capture.py /usr/lib/pysniff

cp "$DIR"/pysniff-capt.service "$DIR"/tmp.service
echo User=$USER >> "$DIR"/tmp.service
echo Group=$(id -gn) >> "$DIR"/tmp.service

sudo mv "$DIR"/tmp.service /lib/systemd/system/pysniff-capt.service

sudo systemctl enable pysniff-capt.service
sudo systemctl start pysniff-capt.service
