# ✅ Guided Lab — Week 1

## Commands: 5W1H + Analogy

### `cd` Command  
**What:** Change directories  
**Why:** Access different folders  
**When:** Whenever you need files elsewhere  
**Where:** Terminal, servers  
**Who:** Everyone  
**How:** `cd /var/log`

💡 *Analogy:* Like double-clicking folders.

➡️ **Try it:** `cd ~` → `pwd` → `ls -la`

---

### Bash Script Example:  
Write `backup-configs.sh`:
- Uses `find` to locate `.conf` files
- Archives them with `tar`
- Deletes originals only if archive succeeds
