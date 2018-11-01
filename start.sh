chown $USER /dev/ttyACM0
chown $USER /dev/ttyUSB0

// docker-compose up &

source venv/bin/activate
python3 smart_home_loop.py