# Dockerized LPJ-GUESS

Dockerized [LPJ-GUESS](https://web.nateko.lu.se/lpj-guess/) builds and runs LPJ-GUESS version 4.1.1 on [alpine linux](https://www.alpinelinux.org/).

## Prerequisites

1. Knowledge of docker basics
2. Knowledge of LPJ-GUESS basics
3. Docker installed and its daemon running.

The easiest is to install [Docker Desktop](https://docs.docker.com/get-docker/) and open it before running the commands in this guide.

## Quickstart

To run the demo data on a single grid cell:

```sh
docker build -t lpj-guess .
docker create --name lpj-guess-temp lpj-guess
docker cp lpj-guess-temp:/lpj-guess/guess_4.1/runs .
docker cp lpj-guess-temp:/lpj-guess/guess_4.1/data .
docker rm lpj-guess-temp
docker run -it --rm -v ./runs:/lpj-guess/guess_4.1/runs \
                    -v ./data:/lpj-guess/guess_4.1/data \
                    -v ./out:/lpj-guess/guess_4.1/out \
                    --name local-lpj-guess lpj-guess
```

When the simulation has completed, the results are available in [./out](./out).

## Detailed Instructions

### Accessing the demo data locally

By default the docker container will use the demo data.
Run the following commands to create a copy of the demo data on you local machine.

```sh
docker build -t lpj-guess .
docker create --name lpj-guess-temp lpj-guess
docker cp lpj-guess-temp:/lpj-guess/guess_4.1/runs .
docker cp lpj-guess-temp:/lpj-guess/guess_4.1/data .
docker rm lpj-guess-temp
```

Now the demo data and instructions folders that LPJ-GUESS is using are also available locally.

This project's folder should now look like this:

```text
.
├── Dockerfile
├── README.md
├── data    # shared with docker containers
│   ├── env
│   ├── gridlist
│   └── ins
└── runs    # shared with docker containers
```

### Running on local data

Optionally edit the instruction files in [./runs](./runs) and/or the data files in [./data/env](./data/env), then run lpj-guess on them:

```sh
docker run -it --rm -v ./runs:/lpj-guess/guess_4.1/runs \
                    -v ./data:/lpj-guess/guess_4.1/data \
                    -v ./out:/lpj-guess/guess_4.1/out \
                    --name local-lpj-guess lpj-guess
```

The results are located in [./out](./out).

By default lpj-guess runs with:

- `-input demo`
- `europe_demo.ins`

To run LPJ-GUESS with custom arguments, pass them to the run command:

```sh
docker run -it --rm -v ./runs:/lpj-guess/guess_4.1/runs \
                    -v ./data:/lpj-guess/guess_4.1/data \
                    -v ./out:/lpj-guess/guess_4.1/out \
                    --name local-lpj-guess lpj-guess \
                    <arg1> <arg2> ...
```

For example, to run using the `cru` input module with the `europe_cru.ins` as instruction file (assuming you have adapted the paths in the instruction file, and have added `cru` data):

```sh
docker run -it --rm -v ./runs:/lpj-guess/guess_4.1/runs \
                    -v ./data:/lpj-guess/guess_4.1/data \
                    -v ./out:/lpj-guess/guess_4.1/out \
                    --name local-lpj-guess lpj-guess \
                    -input cru europe_cru.ins
```

View the LPJ-GUESS help to see the many arguments and configuration options:

```sh
docker run -it --rm -v ./runs:/lpj-guess/guess_4.1/runs \
                    -v ./data:/lpj-guess/guess_4.1/data \
                    -v ./out:/lpj-guess/guess_4.1/out \
                    --name local-lpj-guess lpj-guess \
                    --help
```

### Using an alias

To avoid copying the entire docker command every time you want to run LPJ-GUESS, set an alias for the current bash/sh/zsh session:

```sh
alias guess='docker run -it --rm -v ./runs:/lpj-guess/guess_4.1/runs \
                                 -v ./data:/lpj-guess/guess_4.1/data \
                                 -v ./out:/lpj-guess/guess_4.1/out \
                                 --name local-lpj-guess lpj-guess'
```

Then run LPJ-GUESS like this:

```sh
guess
```

or with custom arguments:

```sh
guess -input cru europe_cru.ins
```

Note that this alias is only defined in the current session. Other terminal instances will not know about it.

## Development mode

```sh
docker build -t lpj-guess .
docker run -it --name demo-lpj-guess lpj-guess
```

This builds a docker image following the instructions in [Dockerfile](/Dockerfile) and tags it `lpj-guess`.
Then it creates and starts a container using the `lpj-guess` image and names it `demo-lpj-guess`.

Exciting right?

But what just happened? Where are the results?

Right now, the results are inside the `demo-lpj-guess` container. You can commit the container as a new image and run it using `sh` as override for the `entrypoint`.

```sh
docker commit demo-lpj-guess demo-lpj-guess
docker run -it --rm --entrypoint sh demo-lpj-guess
```

This drops you in `/lpj-guess/guess_4.1/runs`. The output is in `/lpj-guess/guess_4.1/out`. To read an output file, run:

```sh
cd ../out
less aaet.out
```

To exit the `demo-lpj-guess` command prompt, either press <kbd>CTRL</kbd> + <kbd>D</kbd> or run:

```sh
exit
```

Clean up images and containers used in this example:

```sh
docker rm demo-lpj-guess
docker image rm demo-lpj-guess
```
