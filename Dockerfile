FROM python:3.8-alpine

COPY requirements.txt /tmp/requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
RUN apk add --no-cache --virtual build_deps gcc musl-dev libffi-dev && \
    pip install --prefer-binary --no-cache --no-compile -r /tmp/requirements.txt && \
    apk del build_deps && apk add --no-cache git runuser bash

WORKDIR /opt/arnaldo

ENV PORT lolwut
ENV SERVER lolwut
ENV CHAN lolwut
ENV NICK lolwut
ENV PASSWORD lolwut
ENV SLISTEN lolwut
ENV imgur_client_id lolwut
ENV imgur_client_secret lolwut
ENV REDIS lolwut
ENV RUNAS_USER lolwut
ENV RUNAS_GROUP lolwut
ENV RUNAS_UID 1009
ENV RUNAS_GID 1009

COPY start.sh /start.sh

ENTRYPOINT ["/start.sh"]

CMD ["python", "motorino_d_avviamento.py"]
