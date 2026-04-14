#!/bin/bash

# Parse flags
RUN_FULL=0
while getopts "f" opt; do
  case $opt in
    f)
      RUN_FULL=1
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

echo "======================================"
if [ "$RUN_FULL" -eq 1 ]; then
    echo "Starting Full Fooocus GUI (v2.5.3)..."
    echo "Full Fooocus will be accessible at: http://<your_mac_ip_address>:7865"
else
    echo "Starting Fooocus API..."
    echo "It will be accessible on your network at:"
    echo "http://<your_mac_ip_address>:8888"
fi
echo "======================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$RUN_FULL" -eq 1 ]; then
    # Run only full Fooocus GUI (no API)
    python "$SCRIPT_DIR/scripts/run_full_fooocus.py"
else
    # just starts the server for you; run setup.sh if you have not done so already
    conda run -n fooocus-api --live-stream python main.py --host 0.0.0.0
fi