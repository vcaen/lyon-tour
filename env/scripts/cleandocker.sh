if [ `sudo docker ps -aq | wc -l` -gt 0 ]; then
	echo "Cleaning Docker's containers"
	sudo docker kill $(sudo docker ps -aq);
	sudo docker rm -f $(sudo docker ps -aq);
fi