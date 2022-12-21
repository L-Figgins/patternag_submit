## Building/Running the Project

`docker compose up --build` or to once the images are built `docker compose up`

## Services

### Using the Api

Backend flask api service.

creating jobs
`curl -d '{"resource":"data-10154db7-5c3c-4418-87bf-8e4cbaa312a3.csv"}' -H "Content-Type: application/json" -X POST http://localhost:3000/api/jobs`

retrieving samples
`curl -G -v "http://localhost:3000/api/samples" --data-urlencode "sample_id=10154db7-5c3c-4418-87bf-8e4cbaa312a3"`

#### Migrations

To run alembic migrations run `docker compose exec -it api alembic upgrade head` while the container (api service) is running.

### Processor

The worker service that is listening for Postgres NOTIFY. This example only has one running, but the service could be replicated in a deployment if we were using k8s. This client makes use of FOR SKIP LOCKED in order to support concurrency.

### NGINX

Reverse proxy / webserver forwarding to api. Overkill for development, but would be used in production to forward requests to upstream services.
