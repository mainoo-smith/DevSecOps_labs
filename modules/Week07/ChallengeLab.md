Updated Title: “Runtime Under Siege: Drift, CVEs, and Versioned Service Controls”

🔄 [Updated Challenge 4]
Version-Aware Cross-Environment Call (Service B v2 in Staging)
Dev Service A must explicitly call v2 of Staging Service B — not default or latest.

✅ Step 1: Deploy Staging Service B v2 as a Separate ECS Service
Use a separate ECS service name (e.g. service-b-v2) in the staging namespace.

service_connect_configuration {
  enabled   = true
  namespace = "staging"

  services {
    port_name = "http"
    client_alias {
      dns_name = "service-b-v2"
      port     = 8080
    }
  }
}
This registers service-b-v2.staging as a unique DNS endpoint in ECS Service Connect.

✅ You now have separate service registration for each version.

🧪 Step 2: Dev Service A Calls Staging Service B v2 Explicitly
In dev-service-a:

const response = await axios.get("http://service-b-v2.staging:8080/health");
✅ Only v2 responds. Versioned DNS ensures deterministic behavior and traceable call chain.

❌ Step 3: Prevent Calls to Wrong Version
Calling this should fail:

// Calls unversioned or latest service (not approved)
await axios.get("http://service-b.staging:8080/health");
You can:

Remove service-b registration

Block it via security group (if routed via ALB)

Add pipeline or code checks to validate DNS targets

✅ Outcome: You’ve enforced version-aware routing across environments with Service Connect
🔒 This enables multi-version testing, gradual rollout, and controlled cross-env communication.

Let’s proceed to the updated Security.md, now including HTTPS enforcement strategies in ECS Service Connect. Ready?

You said:
Ready
ChatGPT said:
Here is the updated Security.md for Week 7, now including a dedicated section on enforcing HTTPS within ECS Service Connect.