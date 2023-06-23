I got tired of IFTTT breaking, and with it only allowing two actions for free accounts I decided I could write my own webhook for KASA control.

This is a Flask app that can tie with ngrok (running in a Docker container) to serve up webhooks to discover and control KASA devices on a local network.

Two routines are provided, discover (with an optional device IP address) and toggle. Documentation is available at /documentation.
