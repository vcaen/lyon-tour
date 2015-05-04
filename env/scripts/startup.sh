(python /app/src/server.py 2>&1 | awk '{ print strftime("%c: "), $0; fflush(); }' | tee /app/env/local/logs/server.txt ) > /dev/null &
echo "127.0.0.1 lyon-tour-database" | sudo tee -a /etc/hosts