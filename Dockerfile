# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/fnndsc/mni-conda-base:unofficial

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Parametric Surface Functions" \
      org.opencontainers.image.description="Create surfaces from spherical functions"

WORKDIR /usr/local/src/pl-parmodel-surface

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["parm", "--help"]
