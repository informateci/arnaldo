Arnaldo
=======

Simple IRC bot for fun & profit.

Installation
--------------

```sh
git clone https://github.com/informateci/arnaldo.git
docker build -t arnaldo:latest .
# copy the .env.stub file and use it to create a proper .env
# you can delete the repo now. You won't need it anymore.
docker run -it --rm --name arnaldo_the_magical_bot --env-file .env arnaldo:latest
```
