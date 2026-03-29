#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/agents"

echo "=== Running planner ==="
adk run --replay "$SCRIPT_DIR/planner-input.json" planner

echo ""
echo "=== Running greeter (reads planner output) ==="
adk run --replay "$SCRIPT_DIR/greeter-input.json" greeter
