# resume-painter

Takes a JSON candidate payload and renders it into an HTML report. No AI, no DB.
The JSON structure is defined by the `Dashboard` schema
(`src/services/api/analyses/schemas.py`) and published in Swagger.

**Endpoint:** `POST /api/analyses/dashboard/` → `text/html`
**Swagger:** http://localhost:8000/api/docs/

## Run

```bash
make install && make run     # http://localhost:8000
```

## Example

```bash
curl -X POST http://localhost:8000/api/analyses/dashboard/ \
  -H "Content-Type: application/json" \
  --data-binary @people/dashboard_test_igor_lebedev.json -o report.html
```
