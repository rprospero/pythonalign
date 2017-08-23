#!/bin/bash

curl https://codeload.github.com/rprospero/pythonalign/zip/master > master.zip
unzip -j master.zip
rm master.zip

pip3 install --user virtualenv
python3 -m virtualenv ./
source bin/activate
pip3 install -r requirements.txt
