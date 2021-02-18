DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sudo mkdir -p /usr/lib/pysniff
sudo cp -R "$DIR"/../pysniff /usr/lib/pysniff
sudo cp -R "$DIR"/../capture.py /usr/lib/pysniff

echo User=$USER >> "$DIR"/pysniff-capt.service
echo Group=$(id -gn) >> "$DIR"/pysniff-capt.service

sudo cp "$DIR"/pysniff-capt.service /lib/systemd/system/

sudo systemctl enable pysniff-capt.service
sudo systemctl start pysniff-capt.service