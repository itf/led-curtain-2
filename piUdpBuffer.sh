#!/bin/bash
sudo sysctl -w net.core.rmem_max=16000
sudo sysctl -w net.core.rmem_default=9000
