#!/bin/bash

/bin/pip3.6 install -r requirements.txt

pytest -n 1 --maillinuxjobber=True
