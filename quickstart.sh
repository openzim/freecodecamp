#!/bin/bash

cd openzim
pip install -r requirements.txt
cd ../client
yarn install --frozen-lockfile
yarn lint
yarn test --run
cd ../openzim
python3 fetch.py --filter=02-javascript
python3 prebuild.py basic-javascript ../client/src/assets/curriculum
cd ../client
yarn build
cd ../openzim
python3 ./fcc2zim --source-dir=../client/dist --zim

