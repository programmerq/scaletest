# Example of network service discovery

## Using swarm mode services via `docker stack deploy`

Clone this repo and run the following:

    docker stack deploy -c docker-compose.yml scaletest

Now, hit the nginx service:

    curl http://localhost:80

(replace `localhost` with the ip of your docker host, where applicable)

This nginx is configured to reverse proxy to http://web:8000/. The 'web' service returns its own container id so you can see where the request originated.

In swarm mode, the dns name 'web' will act as a VIP for an IPVS load balancer. This will load balance you in round robin across all instances of the 'web' service. By default, you have one instance of the 'web' service with this docker-compose.yml file.

Let's increase the replica count for the 'web' service. Edit the docker-compose.yml file, and find the services.web.deploy.replicas key. Change it from 1 to 10. Save and exit.

Run this command again:

    docker stack deploy -c docker-compose.yml scaletest

This will update the services to match the new definition. Run the curl command again and again to see the container id change with each request in a round-robin fashion:

    curl http://localhost:80
    curl http://localhost:80
    curl http://localhost:80

Unlike "regular" containers that use DNS round-robin, the routing mesh round robin is handled by the kernel ipvs configuration. There's no need for nginx to wait for the DNS ttl to expire when updating a service. The VIP remains the same, and the ipvs config is updated automatically in the background.

### So what is going on in the background?

The 'docker stack deploy' command is doing something automatically here for us. It inspects the docker-compose.yml file. It discards anything that it doesn't directly support (in this example, the 'build' and 'restart' keys are discarded in favor of using 'image' and 'deploy.restart\_policy'. It creates a network for us (scaletest\_default in this example), and then does `docker service create --net=scaletest_default ...` for each service defined. The things in the 'deploy' key for each service are 'docker service' specific options.

Once the network and services are up and running, we have a running application.


## Using regular containers via `docker-compose`

Clone this repo and run the following:

    docker-compose up -d && docker-compose scale web=10

Now, hit the nginx service:

    curl http://localhost:80

(replace `localhost` with the ip of your docker host, where applicable)

This nginx is configured to reverse proxy to http://web:8000/. The 'web' service returns its own container id so you can see where the request originated.

Each instance of the web container is something that will return its hostname (which happens to be the short container id so we can see which container generated this request).

Nginx honors DNS cache settings, so you may need to wait up to ten minutes before you see requests to all containers after you run the `docker-compose scale` option. If you don't want to wait, just restart the nginx container.

You can see what value is returned by docker's internal DNS service by running the following:

    docker exec -it scaletest_nginx_1 drill web.

or

    docker-compose run nginx drill web.

### So what is going on?

Compose is doing something automatically here for us, it's basically using the `docker run --net-alias` option. For example, when it makes the `scaletest_web_2` container, it is essentially doing

    docker run --net=scaletest_default --name scaletest_web_2 --net-alias web ...

Since both that container and nginx are on the same --net, nginx gets the IP of scaletest_web_2 when it queries the 'web' name, along with any other containers that share the `web` alias.

Nginx has round robin DNS support in its proxy module, and treats the upstream just like any other round robin DNS.
