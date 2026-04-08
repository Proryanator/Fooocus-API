# Get local IP
LOCAL_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)

echo "======================================"
echo "Starting Fooocus API..."
echo "It will be accessible on your network at:"
echo "http://$LOCAL_IP:8888"
echo "======================================"

# just starts the server for you; run setup.sh if you have not done so already
conda run -n fooocus-api --live-stream python main.py --host 0.0.0.0