
---

## `challenge.md`

```markdown
# Challenge Lab – Week 2

### 🧪 Scenario:
Your production EC2 server is exposed and has root login enabled.

**Tasks:**
1. SSH into the instance with your key pair
2. Create a `deployer` user with sudo access
3. Disable password login and root SSH login
4. Setup basic UFW rules to only allow port 22 (SSH)
5. Install `fail2ban` and check its status
6. Create a shell script called `audit.sh` that:
   - Lists logged in users
   - Lists disk usage
   - Lists last 5 login attempts

---

### 🧠 Stretch Goal:
Automate the audit script via cronjob or systemd timer.


=====================================================
# Challenge Lab – Week 2

## Scenario:

You're the platform engineer setting up a staging server for the `backend-api`.

✅ Tasks:
- Create a secure user `pipeline` for automation
- Harden SSH access (no root login, key-based only)
- Set up `fail2ban` and UFW
- Write a `restart-if-down.sh` that checks if `backend-api` is inactive and restarts it

💡 Bonus:
- Use cron to run the health check every hour