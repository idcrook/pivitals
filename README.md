# pivitals
Python program to monitor and log (using MQTT) Raspberry Pi vitals


```shell
# Install a python3 dev setup and other libraries
sudo apt install -y python3-pip python3-venv build-essential \
    python3-setuptools python3-wheel git
```

```
# place a clone of this repo in ~/projects/
mkdir -p ~/projects
cd ~/projects

git clone https://github.com/idcrook/pivitals.git
cd pivitals
```

### create virtualenv

```shell
$ cd ~/projects/pivitals
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install --no-cache-dir -r requirements.txt
```


## test

```shell
(.venv) $ python create_cfg.py
(.venv) $ cp config.example.json config.secrets.json
# EDIT config.secrets.json 
(.venv) $ python 
```