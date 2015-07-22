# Random Noms

## App setup

Start the app locally using `foreman`:

``` bash
    vagrant@vagrant-ubuntu-trusty-32:/vagrant/random-noms$ foreman start web
    02:19:05 web.1  | started with pid 2332
    02:19:05 web.1  | [2015-07-22 02:19:05 +0000] [2332] [INFO] Starting gunicorn 19.3.0
    02:19:05 web.1  | [2015-07-22 02:19:05 +0000] [2332] [INFO] Listening at: http://0.0.0.0:5000 (2332)
    02:19:05 web.1  | [2015-07-22 02:19:05 +0000] [2332] [INFO] Using worker: sync
    02:19:05 web.1  | [2015-07-22 02:19:05 +0000] [2339] [INFO] Booting worker with pid: 2339
```

... and navigate to `localhost` port 5000.

## Social sign-on



## Deployment

Note: app needs a G+ client secrets file called `client_secrets.json`.

