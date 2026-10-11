# Sanitized Version 1.0 source archive

The complete **sanitized** Version 1 source package is stored in this directory as Base64 parts because the connected repository write interface accepts text reliably but not a local binary file handoff.

To reconstruct the ZIP on macOS/Linux:

```bash
cat vancouver-housing-forecasting-v1.0.zip.b64.part* | base64 --decode > vancouver-housing-forecasting-v1.0.zip
unzip vancouver-housing-forecasting-v1.0.zip
```

The archive contains the implementation, scripts, tests, stage contracts and documentation. It intentionally excludes restricted third-party `data/` and large generated `outputs/`, except public notice placeholders.
