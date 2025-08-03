# 🛠️ Week 16 – Guided Lab: Secure Code Practices for Node.js & Python APIs

---

## 🧪 Lab Scope

You’ll:

- Add input validation to Node.js and Python services
- Fix auth bypass by implementing proper role checks (RBAC)
- Apply secure headers (CSP, XSS protection, HSTS)
- Upgrade vulnerable dependencies
- Introduce brute-force protection (rate limiting)
- Run static analysis (Bandit + ESLint security plugins)
- Validate with unit tests

---

## 🔰 Part 1 – Input Validation

### A. Node.js Auth-Service

#### Step 1: Install `express-validator`

```bash
npm install express-validator
Step 2: Add validation middleware to /login
// routes/auth.js
const { body, validationResult } = require('express-validator');

router.post('/login', [
  body('username').isAlphanumeric().notEmpty(),
  body('password').isLength({ min: 8 })
], (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

  // proceed with login
});
✅ Why: Prevents injection, malformed input, and logic errors.

B. Python Notes-Service
Step 1: Install pydantic
pip install pydantic
Step 2: Validate input in Flask route
from pydantic import BaseModel, ValidationError
from flask import request

class NoteInput(BaseModel):
    title: str
    body: str

@app.route('/note', methods=['POST'])
def create_note():
    try:
        data = NoteInput(**request.get_json())
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    # Proceed to store note
✅ Why: Prevents script injection, NoSQL injection, and malformed data storage.

🧑‍⚖️ Part 2 – Role-Based Access Control (RBAC)
Node.js Auth-Service (Admin-Only Route Example)
Step 1: Create checkRole middleware
function checkRole(role) {
  return (req, res, next) => {
    if (req.user?.role !== role) {
      return res.status(403).json({ message: 'Access denied' });
    }
    next();
  };
}
Step 2: Protect routes
router.post('/user/delete', checkRole('admin'), deleteUserHandler);
✅ Why: Fixes broken access control (OWASP A01)

🧱 Part 3 – Secure Headers
A. Node.js (Express)
npm install helmet
const helmet = require('helmet');
app.use(helmet());
✅ Adds:

X-Content-Type-Options

X-XSS-Protection

Content-Security-Policy

Strict-Transport-Security

B. Python (Flask)
pip install flask-talisman
from flask_talisman import Talisman
Talisman(app)
✅ Automatically enforces HTTPS and adds secure headers.

🚫 Part 4 – Rate Limiting (Brute-Force Protection)
Node.js (auth-service)
npm install express-rate-limit
const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
  windowMs: 5 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts'
});

app.post('/login', loginLimiter, loginHandler);
✅ Helps detect/prevent brute-force attacks (OWASP A07).

🔎 Part 5 – Static Code & Dependency Scanning
A. Node.js
npm audit fix
npx eslint --plugin eslint-plugin-security .
B. Python
pip install bandit pip-audit
bandit -r .
pip-audit
✅ SAST + dependency scan → early detection of known issues.

🧪 Part 6 – Unit Testing Security Logic
Example: Node.js
describe('POST /login', () => {
  it('should reject short passwords', async () => {
    await request(app)
      .post('/login')
      .send({ username: 'user', password: '123' })
      .expect(400);
  });
});
Example: Python
def test_invalid_note_input(client):
    response = client.post('/note', json={"title": 1, "body": []})
    assert response.status_code == 400
✅ Ensures validation logic works + prevents regressions.

✅ Completion Checklist
✅	Task
🟢 Input validation implemented in both services	
🟢 Secure headers configured	
🟢 RBAC controls added	
🟢 Rate limiting applied	
🟢 Static & dependency scans run	
🟢 Unit tests validate security logic	
🔐 Key DevSecOps Outcome
Application-level risks mitigated with code-based controls

Proactive scanning and validation tools added to workflow

Secure-by-default patterns introduced in all critical routes


---

Let me know when you're ready for the **Challenge Lab**, where you’ll intentionally exploit vulnerable routes (in a prior commit or branch), then patch them — reinforcing threat awareness and secure coding skills in a real scenario.
You said:
Are you going to cover dynamic application testing too? Then proceed 
ChatGPT said:
Yes — great catch. We’ll cover Dynamic Application Security Testing (DAST) in this module as well. While static analysis scans code and dependencies, DAST simulates real user behavior, probing your live API for vulnerabilities like:

Authentication bypass

Injections (SQL, NoSQL, command)

Misconfigurations

Missing headers

Exposed endpoints

API rate limits

We’ll use tools like:

🔍 OWASP ZAP (intercept proxy + active scanner)

🧪 Nikto or Nuclei (if going deeper later)

🌐 Postman security collection (manual fuzzing)