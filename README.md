# Example of network service discovery

Clone this repo and run the following:

    docker-compose up -d && docker-compose scale web=10

Now, hit the nginx service:

    curl http://localhost:80

(replace `localhost` with the ip of your docker host, where applicable)

This nginx is configured to reverse proxy to http://web:8000/.

Each instance of the web container is something that will return its hostname (which happens to be the short container id so we can see which container generated this request).

Nginx honors DNS cache settings, so you may need to wait up to ten minutes before you see requests to all containers after you run the `docker-compose scale` option.


You can see what value is returned by docker's internal DNS service by running the following:

    docker exec -it scaletest_nginx_1 drill web.

or

    docker-compose run nginx drill web.

## So what is going on?

Compose is doing something manually here for us, it's basically using the 'docker run --net-alias' option. For example, when it makes the `scaletest_web_2` container, it is essentially doing

    docker run --net=scaletest_default --name scaletest_web_2 --net-alias web ...

Since both that container and nginx are on the same --net, nginx gets the IP of scaletest_web_2 when it queries the 'web' name, along with any other containers that share the `web` alias.

Nginx has round robin DNS support in its proxy module, and treats the upstream just like any other round robin DNS.
