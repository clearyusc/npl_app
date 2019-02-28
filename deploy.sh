# For DigitalOcean:
docker build -t nplapp .
docker run --rm -p 80:80 nplapp
