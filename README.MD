# ArcGIS Portal Tools Repository

## Scripts Included

### `env.py`

#### Description:
This script allows sharing of portal url and admin credentials among all script within module for token retrieval and admin functions.

#### Usage:
1. Rename example-env.py -> env.py
2. Configure `env.py` with your base portal URL and admin credentials. Configure additional sections as needed.

---

### `update-portal-item-url.py`

#### Description:
This script updates URLs in ArcGIS portal items owned by a specific user and initiates a full reindex of portal content and items.

#### Usage:
1. Configure `env.py` with your portal URL, admin credentials, old and new URLs, and owner(optional). This will replace the base urls from old -> new, it will leave everything after the base url untouched.
2. Run `python update-portal-item-url.py` to execute the script.

---

### `register-service.py`

#### Description:
This script registers secure services on ArcGIS portal using input from `register-service-input.json`.

#### Input Files

`register-service-input.json`
Sample JSON format for registering services on the ArcGIS portal.

#### How to Run:
1. Configure `env.py` with your portal URL and credentials of user who will own secured service.
2.Fill `register-service-input.json` with your data.
   - See `register-service-input.json` for example data.
   - `services` should contain an array of services to register with `url` and `title`.
3.Run `python register-service.py` to execute the script.


---

### `reindex-portal.py`

#### Description:
This script initiates a full re-index of all portal content.

#### How to Run:
1. Configure `env.py` with your portal URL and admin credentials.
2. Run `python reindex-portal.py` to execute the script.

---

### `list-all-users.py`

#### Description:
This script generates a list of all portal users.

#### How to Run:
1. Configure `env.py` with your portal URL and admin credentials.
2. Run `python list-all-users.py` to execute the script.
