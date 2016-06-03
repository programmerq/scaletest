# Example of network service discovery

Clone this repo and run the following:

    docker-compose up -d && docker-compose scale web=10

Now, hit the nginx service:

    curl http://localhost:80

(replace `localhost` with the ip of your docker host, where applicable)

This nginx is configured to reverse proxy to http://web:8000/.

Each instance of the web container is something that will return its hostname (which happens to be the short container id so we can see which container generated this request).

Nginx honors DNS cache settings, so you may need to wait up to ten minutes before you see requests to all containers after you run the `docker-compose scale` option.
