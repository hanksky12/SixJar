# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.9-buster AS builder

WORKDIR /sixJar

COPY requirements.txt /sixJar
RUN <<EOF
    --mount=type=cache,target=/root/.cache/pip
    apt-get update
    apt-get install vim
    pip3 install -r requirements.txt
EOF

COPY app.py /sixJar
COPY ./app /sixJar/app


ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /