# multi_inventory_checkgt

Steps to create a new tenant (concise)

# Makemigrations

python manage.py makemigrations
python manage.py migrate_schemas --shared

1 Ensure public (central) tenant exists
If not, bootstrap it:
POST to /api/tenants/bootstrap-public/ (or /tenants/bootstrap-public/)
JSON:
{
"subdomain": "public",
"owner": { "email": "admin@public", "password": "pass" }
}

2.Provision the new tenant (preferred)
POST to /api/tenants/provision-tenant/ (or /tenants/provision-tenant/)
Required JSON:
{
"campany_name": "tenant1",
"owner": {
"email": "owner@tenant1.localhost",
"password": "password",

<!-- "is_superuser": true,
"is_staff": true,
"groups": ["managers","staff"] // optional -->

}
}
Notes:
schema_name and the resulting domain (subdomain + BASE_DOMAIN) must be unique.
The endpoint runs provisioning and migrations; it will create the public owner (if missing), create tenant schema, domain, and add the owner to the tenant.

3.Create tenant-scoped groups (optional)
Use tenant subdomain so middleware sets request.tenant, then:
POST to /api/tenants/tenant/groups/
JSON:
{ "name": "managers", "permissions": ["app_label.codename"] }
:- full category CRUD permissions example:
{
"name": "Category Admin",
"permissions": [
"inventory.add_category",
"inventory.change_category",
"inventory.delete_category",
"inventory.view_category"
]
}

4.Create tenant users (optional)
From the tenant subdomain (or via public + tenant_schema option), call tenant-user create:
POST to /api/tenants/tenant-users/ (if route enabled)
JSON:
{
"email":"user@tenant1.localhost",
"password":"password",
"username":"user1",
"is_superuser": false,
"is_staff": false,
"groups": ["managers"]
}
Or use tenant.add_user() in Django shell.

5.Login and obtain token for a specific tenant
Central login with tenant selection:
POST to /api/tenants/token/ with
{
"email":"owner@tenant1.localhost",
"password":"password",
"tenant_schema":"tenant1"
}
Response will include tokens and tenant info.
Alternatively, request token from tenant subdomain URL (middleware will enforce membership).

6.Verify tenant created
Inspect DB or use API GET /api/tenants/ or check domain record.
To inspect user membership:
In Django shell (public schema):
with schema_context(get_public_schema_name()):
u = UserAccount.objects.get(email='owner@tenant1.localhost')
print(list(u.tenants.all()))
Common pitfalls

Missing public tenant: some operations assume it exists.
Password mismatch: owner must have correct password; provisioning creates/updates public user.
Domain/schema uniqueness: ensure schema_name and subdomain not already used.
Routes: If tenants.urls are included under /api/, prefix endpoints with /api/.
Want me to:
