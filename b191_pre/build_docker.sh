#!/bin/bash
NAMESPACE="${1:-codebase_b191_app}"
docker build -t "$NAMESPACE" .