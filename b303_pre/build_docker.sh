#!/bin/bash
NAMESPACE="${1:-codebase_b303_app}"
docker build -t "$NAMESPACE" .