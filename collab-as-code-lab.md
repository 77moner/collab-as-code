# From Zero to "As Code": A Hands-On Lab for Cisco Collaboration Engineers

**Who this is for:** You manage Cisco Collaboration (Webex Calling, CUCM, Control Hub, workspaces) and have never used an IDE, Python, or Git. You want real hands-on reps, not theory.

**How this lab works:** 10 modules, each with numbered exercises. Every exercise builds on the artifact from the previous one — by the end you'll have a working Python/Git project that reads and writes real Webex **and** CUCM data, plus Ansible and Terraform versions of the same task, and hands-on experience with a multi-engineer Git workflow. Don't skip exercises; later ones assume the files from earlier ones exist. Modules 1-6 use Webex (cloud, REST/JSON — the easier starting point); Modules 7-9 shift to CUCM (on-prem, SOAP/XML — a different shape, same underlying ideas); Module 10 simulates a second engineer collaborating on the same repo.

**Time budget:** ~22-28 hours total, doable in evenings/weekends over 4-5 weeks.

**Prerequisites to gather before starting:**
- A laptop (Windows, Mac, or Linux — all fine)
- A free GitHub account (github.com/signup)
- Admin or read access to a Webex Control Hub org (a trial org at developer.webex.com works if you don't want to touch production)
- For Modules 7-9: access to a CUCM publisher with admin rights. If you don't have a lab CUCM, reserve a free **Collaboration sandbox** at developer.cisco.com/site/sandbox (details in Module 7)

---

## Module 0 — Workshop Setup

Goal: get your tools installed once so every later exercise just works.

### Exercise 0.1 — Install VS Code
1. Download from https://code.visualstudio.com and install it.
2. Open it. Install these extensions (Extensions icon in the left sidebar, search each by name):
   - **Python** (by Microsoft)
   - **GitLens**
   - **YAML** (by Red Hat)
   - **HashiCorp Terraform**
3. Open the built-in terminal: `View > Terminal`. You'll live in this for the rest of the lab.

**Checkpoint:** You can open a terminal inside VS Code and it shows a command prompt.

### Exercise 0.2 — Install Git
1. Download from https://git-scm.com/downloads, install with default options.
2. In the VS Code terminal, run:
   ```
   git --version
   ```
3. Set your identity (used to label every change you make):
   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

**Checkpoint:** `git --version` prints a version number, not an error.

### Exercise 0.3 — Install Python
1. Download Python 3.11+ from https://python.org/downloads (Windows: check "Add Python to PATH" during install).
2. Verify:
   ```
   python3 --version
   pip3 --version
   ```
   (On Windows it may just be `python` and `pip` — either works.)

**Checkpoint:** Both commands print version numbers.

### Exercise 0.4 — Create your project folder
```
mkdir collab-as-code
cd collab-as-code
```
Open this folder in VS Code (`File > Open Folder`). Everything you build lives here.

---

## Module 1 — Git Fundamentals

Goal: understand version control well enough to never fear `git status` again. You'll track a plain config file first — no code needed yet — so you focus purely on the Git mental model.

### Exercise 1.1 — Init a repo and make your first commit
```
git init
```
Create a file called `notes.md` with this content:
```
# My as-code learning notes
Day 1: installed Git, Python, VS Code.
```
Then:
```
git add notes.md
git status
git commit -m "Initial commit: setup notes"
```
**Why this matters:** `git add` stages a change, `git commit` saves a permanent snapshot with a message. This is the exact workflow you'll use to track every config change you ever push to a real system.

**Checkpoint:** `git log` shows one commit with your message.

### Exercise 1.2 — Make changes and see diffs
Edit `notes.md`, add a line: `Day 2: learned about staging.` Then:
```
git diff
```
This shows exactly what changed before you commit — this is how you'd review a config change before applying it to CUCM or Webex.
```
git add notes.md
git commit -m "Add day 2 notes"
```

### Exercise 1.3 — Branching
Branches let you try something without touching the "known good" version.
```
git branch experiment
git checkout experiment
```
Edit `notes.md`: add `Day 3: trying a branch.` Commit it:
```
git add notes.md
git commit -m "Day 3 notes on experiment branch"
```
Switch back to main and notice the change is gone:
```
git checkout main
cat notes.md
```
**Why this matters:** This is exactly how you'd stage a risky dial-plan or Control Hub template change without affecting the version everyone else uses.

### Exercise 1.4 — Merge
```
git merge experiment
cat notes.md
```
Your Day 3 line is now in `main`.

**Checkpoint:** `git log --oneline --graph` shows the branch history merging together.

### Exercise 1.5 — Push to GitHub
1. On github.com, create a new **empty** repository named `collab-as-code`.
2. Connect and push:
   ```
   git remote add origin https://github.com/YOUR-USERNAME/collab-as-code.git
   git branch -M main
   git push -u origin main
   ```
3. Refresh the GitHub page — your commits are there.

**Checkpoint:** Your commit history is visible on GitHub, not just on your laptop.

*Module 1 complete. You now have real muscle memory for add/commit/branch/merge/push — this repo keeps growing through every remaining module.*

---

## Module 2 — Python Basics (just enough)

Goal: not "learn Python," but "learn the ~20% of Python used for automation." Every exercise here writes a `.py` file into the same repo.

### Exercise 2.1 — Hello, variables
Create `hello.py`:
```python
engineer_name = "Your Name"
product = "Webex Calling"
print(f"{engineer_name} manages {product}")
```
Run it:
```
python3 hello.py
```
Commit it (`git add hello.py`, `git commit -m "Add hello script"`).

### Exercise 2.2 — Lists and loops
Create `workspaces.py`:
```python
workspaces = ["Lobby Cisco Board", "HQ Floor 3 Room A", "HQ Floor 3 Room B"]

for ws in workspaces:
    print(f"Checking workspace: {ws}")
```
Run and commit it.

**Why this matters:** Every bulk operation you'll ever do against Webex/CUCM is "loop over a list of things, do the same action to each."

### Exercise 2.3 — Dictionaries and JSON
Create `sample_device.py`:
```python
import json

device = {
    "name": "Lobby Cisco Board",
    "type": "roomdesk",
    "ip": "10.10.10.5",
    "connected": True
}

print(device["name"])
print(json.dumps(device, indent=2))
```
Run it. Notice the output looks exactly like what an API returns.

**Why this matters:** Every REST API response and Terraform variable file is JSON underneath. This dictionary-to-JSON mapping is the single most reused concept in the rest of the lab.

### Exercise 2.4 — Functions
Create `functions.py`:
```python
def is_online(device):
    return device["connected"]

devices = [
    {"name": "Board A", "connected": True},
    {"name": "Board B", "connected": False},
]

for d in devices:
    status = "ONLINE" if is_online(d) else "OFFLINE"
    print(f"{d['name']}: {status}")
```
Commit all four files together:
```
git add hello.py workspaces.py sample_device.py functions.py
git commit -m "Module 2: Python basics"
git push
```

**Checkpoint:** You can explain, in your own words, what a dictionary is and why it maps to JSON.

---

## Module 3 — Talking to a Real API (Webex)

Goal: call the actual Webex REST API from Python. This is where it stops being abstract.

### Exercise 3.1 — Get a Webex API token
1. Go to https://developer.webex.com, log in with your Webex/Control Hub credentials.
2. Go to "My Webex Apps" (or the docs landing page) and copy your **personal access token** (valid 12 hours — fine for this lab).

### Exercise 3.2 — Explore with Postman first (no code)
1. Install Postman (postman.com/downloads).
2. New request: `GET https://webexapis.com/v1/people/me`
3. Under Authorization, choose "Bearer Token" and paste your token.
4. Send it. You get back JSON describing your own user account.

**Why this matters:** Postman lets you see exactly what the API returns before you write a single line of code to parse it. Always prototype a new API call here first.

### Exercise 3.3 — Same call, in Python
Install the `requests` library:
```
pip3 install requests
```
Create `webex_me.py`:
```python
import requests

TOKEN = "PASTE_YOUR_TOKEN_HERE"
headers = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get("https://webexapis.com/v1/people/me", headers=headers)
data = response.json()

print(f"Name: {data['displayName']}")
print(f"Email: {data['emails'][0]}")
```
Run it. You should see your own name and email printed from a live API call.

**Do NOT commit your token.** Create a file named `.gitignore` in the folder with this content:
```
.env
*.token
```
We'll fix the token exposure properly in the next exercise.

### Exercise 3.4 — Stop hardcoding secrets
Create a file `.env`:
```
WEBEX_TOKEN=paste_your_real_token_here
```
Install a helper library:
```
pip3 install python-dotenv
```
Rewrite `webex_me.py`:
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("WEBEX_TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get("https://webexapis.com/v1/people/me", headers=headers)
data = response.json()

print(f"Name: {data['displayName']}")
print(f"Email: {data['emails'][0]}")
```
Confirm `.env` is listed in `.gitignore`, then commit and push everything **except** `.env`:
```
git add webex_me.py .gitignore
git commit -m "Module 3: first live Webex API call"
git push
```

**Why this matters:** This is the #1 real-world habit — credentials never go into Git. Every tool from here on (Ansible, Terraform) follows this same pattern.

### Exercise 3.5 — List your org's workspaces
Create `list_workspaces.py`:
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("WEBEX_TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get("https://webexapis.com/v1/workspaces", headers=headers)
workspaces = response.json()["items"]

for ws in workspaces:
    print(f"{ws['displayName']} — capacity: {ws.get('capacity', 'n/a')}")
```
Run it against your real (or trial) org.

**Checkpoint:** You've now done the full loop — Postman to explore, Python to script, `.env` to protect the secret, Git to version it. This is a real automation, small as it is.

Commit and push.

---

## Module 4 — Ansible

Goal: understand Ansible's "describe the steps, in YAML" model, using your Webex API as the target system (Ansible doesn't need a Cisco-specific module for this — its `uri` module can call any REST API, which is exactly how many collaboration teams use it today).

### Exercise 4.1 — Install Ansible
```
pip3 install ansible
ansible --version
```

### Exercise 4.2 — Your first playbook
Create `inventory.ini`:
```ini
[local]
localhost ansible_connection=local
```
Create `list_workspaces.yml`:
```yaml
---
- name: List Webex workspaces
  hosts: local
  gather_facts: false
  vars:
    webex_token: "{{ lookup('env', 'WEBEX_TOKEN') }}"
  tasks:
    - name: Call Webex API
      uri:
        url: https://webexapis.com/v1/workspaces
        method: GET
        headers:
          Authorization: "Bearer {{ webex_token }}"
        return_content: true
      register: result

    - name: Print workspace names
      debug:
        msg: "{{ item.displayName }}"
      loop: "{{ result.json.items }}"
```
Load your token into the environment and run it:
```
export WEBEX_TOKEN=paste_your_real_token_here
ansible-playbook -i inventory.ini list_workspaces.yml
```
(On Windows PowerShell: `$env:WEBEX_TOKEN="paste_your_real_token_here"`)

**Why this matters:** Notice this does the *same thing* as `list_workspaces.py`, but declaratively — you described tasks in YAML instead of writing procedural Python. This is Ansible's whole pitch: readable-by-anyone automation, no programming required, which is why network/collab teams adopt it faster than Python scripting.

### Exercise 4.3 — Add idempotence thinking
Modify the playbook to only print workspaces with a name containing "Room":
```yaml
    - name: Print only Room workspaces
      debug:
        msg: "{{ item.displayName }}"
      loop: "{{ result.json.items }}"
      when: "'Room' in item.displayName"
```
Run it again. **Why this matters:** "idempotent" means running the playbook 10 times gives the same end state as running it once — no duplicate actions. This is the property that makes "as code" tools safe to re-run, unlike a one-off script.

Commit everything:
```
git add inventory.ini list_workspaces.yml
git commit -m "Module 4: Ansible playbook hitting Webex API"
git push
```

**Checkpoint:** You can explain the difference between what you did in Python (procedural — "do this, then this") vs. Ansible (declarative task list, with built-in looping/conditionals, no explicit HTTP library needed).

---

## Module 5 — Terraform

Goal: understand *true* declarative infrastructure — you describe the end **state**, and Terraform figures out the steps, tracking what it created in a state file so it knows what to change later.

### Exercise 5.1 — Install Terraform
Download from https://developer.hashicorp.com/terraform/downloads, or:
```
# Mac
brew install terraform
# Windows (with Chocolatey)
choco install terraform
```
Verify:
```
terraform -version
```

### Exercise 5.2 — Your first Terraform config (no cloud yet)
Create a new subfolder `terraform-intro/` and inside it, `main.tf`:
```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "example" {
  filename = "${path.module}/hello.txt"
  content  = "Managed by Terraform!"
}
```
Run:
```
cd terraform-intro
terraform init
terraform plan
terraform apply
```
Type `yes` when prompted. Look at the `hello.txt` file that appeared — Terraform created it and is now tracking it.

**Why this matters:** `terraform plan` shows you exactly what will change *before* it happens — this "preview then apply" pattern is what makes Terraform safer than ad-hoc scripts for infrastructure changes.

### Exercise 5.3 — Change the desired state
Edit `main.tf`, change the content string to `"Managed by Terraform! v2"`. Run:
```
terraform plan
```
Notice it tells you it will **update in-place** — it diffed your desired state against the real file automatically.
```
terraform apply
```

### Exercise 5.4 — Destroy
```
terraform destroy
```
Type `yes`. The file is gone. **Why this matters:** Terraform can tear down exactly what it built — this is huge for temporary lab/test environments (e.g., spinning up and tearing down a test Webex location for a demo).

### Exercise 5.5 — The Webex Terraform provider (conceptual + real if you want to go further)
Cisco/community-maintained Terraform providers exist for Webex (e.g., managing locations, users, workspaces as code). In `terraform-webex/main.tf`:
```hcl
terraform {
  required_providers {
    webex = {
      source = "CiscoDevNet/webex"
    }
  }
}

provider "webex" {
  # token pulled from WEBEX_ACCESS_TOKEN environment variable
}

data "webex_workspace_list" "all" {}

output "workspace_names" {
  value = [for w in data.webex_workspace_list.all.items : w.display_name]
}
```
```
export WEBEX_ACCESS_TOKEN=paste_your_real_token_here
terraform init
terraform plan
```
This uses a **data source** (read-only, no changes made) so it's safe to run against your real org — it just lists workspaces, output as Terraform variables you could feed into other resources.

**Checkpoint:** You can explain, in one sentence each, the difference between Ansible (procedural task list, good for one-time or ordered actions) and Terraform (declarative state management, good for infrastructure that needs to be tracked and torn down/rebuilt).

Commit the Terraform folders (add a `.gitignore` entry for `.terraform/` and `*.tfstate*` first — state files can contain sensitive data):
```
echo ".terraform/
*.tfstate
*.tfstate.backup" >> .gitignore
git add terraform-intro terraform-webex .gitignore
git commit -m "Module 5: Terraform basics + Webex provider"
git push
```

---

## Module 6 — Capstone: Bring It Together

Goal: one small but *real* project that exercises everything — Git branching, Python + API, and a README documenting it like a real internal tool.

### Exercise 6.1 — Branch for a feature
```
git checkout -b feature/workspace-report
```

### Exercise 6.2 — Build a small reporting script
Create `workspace_report.py`:
```python
import os
import csv
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("WEBEX_TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get("https://webexapis.com/v1/workspaces", headers=headers)
workspaces = response.json()["items"]

with open("workspace_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Capacity", "Type"])
    for ws in workspaces:
        writer.writerow([ws["displayName"], ws.get("capacity", "n/a"), ws.get("type", "n/a")])

print(f"Report written for {len(workspaces)} workspaces.")
```
Run it — you now have a real CSV export of your org's workspaces, generated by a script you wrote from scratch.

### Exercise 6.3 — Write a README (documentation as code)
Create `README.md`:
```markdown
# Collab As-Code Learning Project

Scripts and configs built while learning Git, Python, Ansible, and Terraform
for Cisco Collaboration automation.

## Setup
1. Copy `.env.example` to `.env` and add your Webex API token.
2. `pip3 install -r requirements.txt`

## Scripts
- `workspace_report.py` — exports all Webex workspaces to CSV
- `list_workspaces.yml` — Ansible equivalent
- `terraform-webex/` — Terraform data source reading workspaces
```
Create `requirements.txt`:
```
requests
python-dotenv
```
Create `.env.example` (a safe template with no real secret):
```
WEBEX_TOKEN=your_token_here
```

### Exercise 6.4 — Merge back via pull request (the real workflow)
```
git add workspace_report.py README.md requirements.txt .env.example
git commit -m "Capstone: workspace CSV report + docs"
git push -u origin feature/workspace-report
```
On GitHub, open a **Pull Request** from `feature/workspace-report` into `main`. Review your own diff, then click "Merge."

**Why this matters:** This PR-based flow — branch, change, review, merge — is exactly how real infrastructure-as-code teams gate changes before they touch production systems. You just did it end to end.

### Exercise 6.5 — Pull the merged result locally
```
git checkout main
git pull
```

**Checkpoint — you're done when you can:**
- Explain Git add/commit/branch/merge/push without notes
- Read basic Python: variables, loops, dicts, functions, JSON
- Call a REST API and parse its JSON response
- Read an Ansible playbook and know what each task does
- Read a Terraform `.tf` file and predict what `plan` would show
- Explain when you'd reach for Ansible vs. Terraform vs. a plain Python script

---

## Module 7 — CUCM Fundamentals: AXL

Everything so far used Webex's REST/JSON API, which is the easy case. CUCM is older and uses **AXL** (Administrative XML Layer) — a SOAP/XML API, not REST/JSON. Different shape, same underlying idea: authenticate, send a request, parse a structured response. This module gets you access and gets one raw call working before you touch any library.

### Exercise 7.1 — Get a CUCM to practice against
You need admin access to a CUCM publisher. Two realistic options:
- **Cisco DevNet Sandbox (recommended if you don't have a lab CUCM):** go to https://developer.cisco.com/site/sandbox, search "Collaboration," and **reserve** (not "Always-On" — AXL needs full admin access) a Collaboration lab. You'll get a VPN profile and CUCM Publisher IP/credentials by email.
- **Your own lab CUCM**, if you have one — a CUCM under a CML/VMware lab works identically.

Once connected, log into CUCM Administration and confirm the **AXL Web Service** is running: `Cisco Unified Serviceability > Tools > Control Center - Feature Services`.

### Exercise 7.2 — Create an AXL-enabled application user
In CUCM Administration:
1. `User Management > Application User > Add New`
2. Create a user (e.g. `axladmin`) with a password.
3. Under **Permissions Information**, add the user group **Standard AXL API Access**.

**Why this matters:** just like the Webex token, this is a dedicated service identity — never use your own admin login for scripted access. Same principle as Exercise 3.4, different platform.

### Exercise 7.3 — Your first raw AXL call (no library, just to see the shape)
AXL is SOAP: you POST an XML envelope to a URL and get XML back. In Postman:
1. New request: `POST https://<CUCM-IP>:8443/axl/`
2. Auth: Basic Auth, using your `axladmin` credentials.
3. Headers: `Content-Type: text/xml`, `SOAPAction: CUCM:DB ver=<your version> getCCMVersion`
4. Body (raw, XML):
   ```xml
   <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/1.0">
     <soapenv:Body>
       <ns:getCCMVersion>
         <processNodeName/>
       </ns:getCCMVersion>
     </soapenv:Body>
   </soapenv:Envelope>
   ```
5. Send it (you'll likely need to disable SSL certificate verification in Postman settings for a lab system with a self-signed cert).

You get back XML containing the CUCM version. **Compare this mentally to Exercise 3.2** — same idea (ask the system a question, get structured data back), completely different envelope format. This is the core adjustment moving from Webex to CUCM: JSON in curly braces vs. XML in angle brackets.

**Checkpoint:** you got a version string back from real CUCM, in raw XML, with no library involved yet.

---

## Module 8 — CUCM Automation in Python

Hand-building SOAP XML gets painful fast. This module uses a library that wraps it for you — same pattern as `requests` wrapping raw HTTP in Module 3.

### Exercise 8.1 — Install ciscoaxl
```
pip3 install ciscoaxl
```
This library wraps the AXL SOAP calls into simple Python method calls (`get_users()`, `get_phone()`, etc.) so you work with plain dictionaries, not hand-written XML.

### Exercise 8.2 — List CUCM users
Add your CUCM credentials to `.env` (same pattern as `WEBEX_TOKEN` — never hardcode):
```
CUCM_HOST=10.10.20.1
CUCM_USER=axladmin
CUCM_PASS=your_password
CUCM_VERSION=12.5
```
Create `cucm_list_users.py`:
```python
import os
from dotenv import load_dotenv
from ciscoaxl import axl

load_dotenv()

ucm = axl(
    username=os.getenv("CUCM_USER"),
    password=os.getenv("CUCM_PASS"),
    cucm=os.getenv("CUCM_HOST"),
    cucm_version=os.getenv("CUCM_VERSION"),
)

users = ucm.get_users()
for user in users:
    print(f"User ID: {user.userid}, Last Name: {user.lastName}, First Name: {user.firstName}")
```
Run it. **Compare to `webex_me.py` from Exercise 3.3** line by line: same shape — load credentials, authenticate, call, loop over the result. The transport underneath (SOAP vs REST) is now hidden from you by the library, exactly like `requests` hid raw HTTP from you.

### Exercise 8.3 — Look up one phone
```python
phone = ucm.get_phones("SEPAAABBBCCCDDD")
if phone:
    # Assuming phone is a list of objects based on the traceback error
    p = phone[0]
    print(f"Description: {p.description}")
    print(f"CSS: {p.callingSearchSpaceName}")
else:
    print("Phone not found.")
```
Run it against a device that exists in your sandbox topology (check the sandbox's device list/topology diagram for a real name).

### Exercise 8.4 — Commit it
```
git add cucm_list_users.py cucm_list_phone.py .env.example
git commit -m "Module 8: CUCM automation via ciscoaxl"
git push
```
(Update `.env.example` with placeholder CUCM values too — never the real ones.)

**Checkpoint:** you can explain why `ciscoaxl` for CUCM plays the same role `requests` + Webex played earlier — a library that turns a network protocol you don't want to hand-write into plain Python objects.

---

## Module 9 — CUCM in Ansible

Cisco publishes real example playbooks for this pattern (`CiscoDevNet/axl-ansible-examples` on GitHub) — worth browsing after this exercise. Here you'll build a minimal version yourself so you understand every line.

### Exercise 9.1 — Install the XML-parsing collection
Ansible's built-in `uri` module can POST the SOAP XML, but you need a helper to parse the XML *response*:
```
ansible-galaxy collection install community.general
```

### Exercise 9.2 — A playbook that gets the CUCM version
Create `cucm_version.yml`:
```yaml
---
- name: Get CUCM version via AXL
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    cucm_host: "{{ lookup('env', 'CUCM_HOST') }}"
    cucm_user: "{{ lookup('env', 'CUCM_USER') }}"
    cucm_pass: "{{ lookup('env', 'CUCM_PASS') }}"
  tasks:
    - name: Call AXL getCCMVersion
      ansible.builtin.uri:
        url: "https://{{ cucm_host }}:8443/axl/"
        method: POST
        force_basic_auth: true
        url_username: "{{ cucm_user }}"
        url_password: "{{ cucm_pass }}"
        headers:
          Content-Type: text/xml
        body: >
          <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/1.0">
            <soapenv:Body>
              <ns:getCCMVersion>
                <processNodeName/>
              </ns:getCCMVersion>
            </soapenv:Body>
          </soapenv:Envelope>
        validate_certs: false
        return_content: true
      register: response

    - name: Parse the version out of the XML response
      community.general.xml:
        xmlstring: "{{ response.content }}"
        xpath: //version
        content: text
      register: parsed

    - name: Show the version
      debug:
        msg: "CUCM version is {{ parsed.matches[0].version }}"
```
Export your CUCM env vars and run:
```
export CUCM_HOST=10.10.20.1
export CUCM_USER=axladmin
export CUCM_PASS=your_password
ansible-playbook -i inventory.ini cucm_version.yml
```

**Reading it like Module 4 taught you:** task 1 sends the same raw SOAP envelope you POSTed by hand in Exercise 7.3, `register` saves the raw XML response, task 2 uses `community.general.xml` to pull just the `<version>` value out of that XML (this is the XML equivalent of `data['displayName']` pulling one field out of a JSON dict back in Module 3), task 3 prints it.

**Why this matters:** this is close to exactly what Cisco's own `axl-ansible-examples` repo does for real provisioning tasks (adding lines, phones, device pools) — same `uri` + `community.general.xml` pattern, just longer SOAP bodies.

Commit:
```
git add cucm_version.yml
git commit -m "Module 9: CUCM version check via Ansible + AXL"
git push
```

**Checkpoint:** you can explain why parsing an XML response needs an extra step (`community.general.xml`) that JSON never needed — JSON parses natively into Python dicts/Ansible variables, XML needs a query language (XPath) to pull one value out.

---

## A note on Terraform and CUCM

You'll notice there's no CUCM equivalent of Module 5's Webex provider exercise. That's not an oversight — **there is no official Terraform provider for CUCM**, and that's realistic, not a gap in your learning. Terraform's model (track a resource's full lifecycle, diff desired vs. actual state, tear it down cleanly) fits cloud/API-native platforms like Webex well. On-prem AXL-based systems like CUCM are almost universally automated with **Ansible or plain Python** instead — because most CUCM automation is "run this provisioning task" (imperative), not "declare this resource should permanently exist and be reconciled" (declarative). Knowing *when a tool doesn't apply* is as useful as knowing when it does — if you ever see a "Terraform for CUCM" claim, treat it skeptically and verify.

---

## Module 10 — Collaborating with Git (Simulating a Second Engineer)

Goal: everything so far has been solo. Real "as code" work happens on a team, where changes land through branches, pull requests, and code review before hitting the shared `main`. You'll simulate this with two local clones of the same repo — no second person or GitHub account needed.

### Exercise 10.1 — Set up "Engineer B"
Your existing folder (with Modules 1-9 committed) is **Engineer A**. Clone the same repo into a second folder to act as **Engineer B**, joining the project fresh:
```
cd ~/                     # anywhere outside your existing repo folder
git clone https://github.com/YOUR-USERNAME/collab-as-code.git collab-as-code-engineer2
cd collab-as-code-engineer2
```
Give this clone its own local identity (scoped to this folder only, not `--global`, so your real identity elsewhere is untouched):
```
git config user.name "Engineer Two"
git config user.email "engineer2@example.com"
```
**Checkpoint:** `git log -1` in this folder shows the same last commit as your original repo — it's a true clone of shared history.

### Exercise 10.2 — Engineer B builds on a branch
```
git checkout -b feature/cucm-automation
```
If you haven't already done Modules 7-9 work in this folder, do (or redo) a small piece of it here — e.g. create `cucm_list_users.py` from Exercise 8.2, with its own `.env` (never committed, per Exercise 3.4's habit). Commit and push the branch:
```
git add cucm_list_users.py
git commit -m "Add CUCM user listing via ciscoaxl"
git push -u origin feature/cucm-automation
```
**Why this matters:** this is exactly what happens when a teammate picks up new work — they branch, they don't touch `main` directly, and their changes are invisible to everyone else until pushed and reviewed.

### Exercise 10.3 — Open and review a pull request
On GitHub, open a PR from `feature/cucm-automation` into `main`. Open the **"Files changed"** tab and read it the way you'd review a colleague's work — look for a hardcoded secret, an unclear commit message, or logic you'd question. Leave at least one comment on a line, even though it's your own PR.

**Checkpoint:** you can point to one thing in the diff you'd have asked a real colleague to change before merging.

### Exercise 10.4 — Merge and sync back as Engineer A
Merge the PR on GitHub. Then, back in your **original** folder:
```
cd ~/collab-as-code
git checkout main
git pull
```
Confirm `cucm_list_users.py` now exists here, even though "Engineer A" never wrote it directly — it arrived purely through the shared Git history.

### Exercise 10.5 — Force and resolve a merge conflict
This is the mechanic behind every "merge conflict" you'll hear referenced on a real team — worth doing once deliberately so it's not scary later.

1. **As Engineer A**, edit `README.md` — add a line under the Scripts section — then commit and push straight to `main`:
   ```
   git add README.md
   git commit -m "Engineer A: update README"
   git push
   ```
2. **As Engineer B** (`collab-as-code-engineer2`), *before* pulling that change, edit the exact same line in `README.md` differently, and commit:
   ```
   git add README.md
   git commit -m "Engineer B: update README"
   ```
3. Now try to bring in Engineer A's change:
   ```
   git checkout main
   git pull origin main
   ```
   Git reports a conflict and marks the file:
   ```
   <<<<<<< HEAD
   Engineer B's line
   =======
   Engineer A's line
   >>>>>>> origin/main
   ```
4. Open `README.md`, decide what the final combined line should say, delete the `<<<<<<<`, `=======`, `>>>>>>>` markers by hand, save, then:
   ```
   git add README.md
   git commit -m "Resolve README merge conflict"
   git push
   ```

**Why this matters:** a merge conflict isn't Git being broken — it's Git correctly refusing to silently pick a winner when two people changed the same lines, and asking a human to decide. This is precisely the situation you'd hit if two engineers both edited an Ansible variable file or a Terraform `.tf` resource in the same week.

**Checkpoint — you're done when you can:**
- Explain why Engineer B's branch was invisible to Engineer A until it was pushed and merged
- Read a GitHub PR diff and identify at least one thing worth a review comment
- Resolve a merge conflict by hand without panicking at the `<<<<<<<` markers

---

## Where to go next
- Browse Cisco's own `CiscoDevNet/axl-ansible-examples` and `CiscoDevNet/axl-python-zeep-samples` repos on GitHub — real, more complete versions of what you just built (adding lines, phones, partitions, device pools).
- Look at Cisco DevNet's Webex Calling and Control Hub API sandboxes for more endpoints to script against.
- Once comfortable, try converting one *real*, low-risk, repetitive task you currently do by hand — in Control Hub **or** CUCM Administration — into a script or playbook.
