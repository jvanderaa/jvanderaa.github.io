# OSNM Design Builder address example

Runnable source for the blog post **Repeatable Network Design With Nautobot Design Builder**.
Pinned to Nautobot 3.2.7 and Design Builder 3.1.2. The data-center and two branch
designs reproduce the book's synthetic topology: 3 locations, 3 racks, 13 devices,
26 interfaces, and 13 cables. Only Nautobot records are changed.

## Run the lab

Requires Docker Compose and Python 3. Run these commands from this directory:

```bash
python3 scripts/init_env.py
docker compose up -d --build
docker compose ps
```

Wait for the web container to be healthy, then:

```bash
docker compose exec -T nautobot nautobot-server shell --interface python < scripts/seed_catalog.py
python3 scripts/lab_api.py fabric --dry-run
python3 scripts/lab_api.py fabric
python3 scripts/lab_api.py site1 --dry-run
python3 scripts/lab_api.py site1
python3 scripts/lab_api.py site2
python3 scripts/lab_api.py site1-repeat
python3 scripts/verify_topology.py
python3 scripts/verify_address_api.py
```

UI: <http://127.0.0.1:8089/>. The initializer creates independent credentials in
`.lab.env`; they are excluded from Git and the downloadable package. The username
is `blog-admin`. Read your generated password locally from that file.

The Compose project is `osnm-design-address`, with its own database and media volumes.
Stop it with `docker compose stop`; resume with `docker compose up -d`.
Rebuild with `docker compose up -d --build` after changing Jobs or templates.

## Physical address behavior

- A new branch requires a nonblank physical address.
- An existing branch can reuse its stored address by leaving the form field blank.
- A supplied address updates `Location.physical_address` in the named deployment.
- Dry run rolls back address and inventory changes.
- Addresses are synthetic examples; the Job performs no geocoding or address lookup.

The form field is optional at the field level because context validation decides
whether an address already exists. `BranchContext.site_address` resolves that value.
The shared template writes the address only for branches, leaving DC1 unchanged.
`string | tojson` unwraps the context value and quotes the address safely for YAML,
including line breaks and embedded quotes.

The template requires the catalog populated by `seed_catalog.py`. The full design
also uses `CableConnectionExtension`, enabled in each Job's metadata. Location
names are assumed unique within this lab's Branch type.

## Tests

On a seeded lab with the fabric deployed and Ethernet3 still free, run:

```bash
docker compose exec -T nautobot nautobot-server shell --interface python < scripts/test_address.py
```

These four form/context/template tests cover required new-site addresses, multiline
input, YAML rendering, and reuse of an existing address. They roll back their temporary Location.
After deploying both branches, `verify_address_api.py` exercises actual Jobs to
check persistence, dry-run rollback, quoted/multiline YAML, blank reuse, and repeat
execution. It restores site1's example address at the end. Run the complete sequence
above in a fresh lab; form tests need an unused branch WAN port.

After seeding the catalog and deploying the fabric, `python3 scripts/run_verification.py`
runs the fabric dry run, branch designs, and API checks together. It generates the
required evidence files itself.

Job helpers save submission IDs in `evidence/` before polling. If a helper times out,
inspect that existing JobResult rather than blindly submitting it again.

## Refresh the blog downloads

From the repository checkout, run:

```bash
python3 examples/osnm-design-builder/scripts/package_lab.py
```

This refreshes the post's standalone template and ZIP using an explicit source
allowlist. Credentials, runtime JobResults, caches, and database contents are excluded.
`examples/` stays in Git; Hugo publishes only the downloads in the post's page bundle.

## Sources

- [Design development](https://docs.nautobot.com/projects/design-builder/en/stable/user/design_development/)
- [Design lifecycle](https://docs.nautobot.com/projects/design-builder/en/stable/user/design_lifecycle/)
- [Locations](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/location/)
