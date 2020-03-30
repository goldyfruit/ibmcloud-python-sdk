#!/bin/env bash

export IC_CONFIG_FILE="test-credentials.yaml"

nosetests tests --rednose --verbose
