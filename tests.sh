#!/bin/env bash

export IC_CONFIG_FILE="fake-credential.yml"

nosetests tests --rednose --verbose
