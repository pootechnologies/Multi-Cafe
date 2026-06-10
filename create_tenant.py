import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multi_inventory_check.settings')
import django
django.setup()
from tenants.models import Tenant, Domain

t = Tenant(schema_name='tenant1', name='Tenant 1')
t.save()
Domain.objects.create(domain='tenant1.localhost', tenant=t, is_primary=True)
print('CREATED', t.schema_name)


# def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         reference = serializer.validated_data["reference"]

#         try:
#             payment = TenantPayment.objects.get(reference=reference)
#             if not payment:
#                 return Response({"detail": "Invalid reference"}, status=status.HTTP_404_NOT_FOUND)
#             if payment.tenant != request.tenant:
#                 return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
#         except TenantPayment.DoesNotExist:
#             return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

#         headers = {
#             # Use secret key for server-to-server verification
#             "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
#             "Content-Type": "application/json",
#         }

#         # Verify payment with Chapa (robust error handling and debug info)
#         try:
#             response = requests.get(f"{CHAPA_BASE_URL}/transaction/verify/{reference}", headers=headers, timeout=10)
#         except requests.RequestException as exc:
#             return Response({"detail": "Failed to verify payment with Chapa", "error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

#         if not response.ok:
#             try:
#                 body = response.json()
#             except Exception:
#                 body = response.text
#             return Response({"detail": "Failed to verify payment with Chapa", "chapa_response": body, "status_code": response.status_code}, status=status.HTTP_502_BAD_GATEWAY)

#         chapa_response = response.json()
#         # Chapa may return data.status as 'success' (test) or 'successful' (live); accept both
#         chapa_data_status = chapa_response.get("data", {}).get("status")
#         if chapa_response.get("status") != "success" or chapa_data_status not in ("successful", "success"):
#             return Response({"detail": "Payment verification failed", "chapa_response": chapa_response}, status=status.HTTP_400_BAD_REQUEST)

#         # Update payment record
#         if chapa_response.get("status") == "success" and chapa_data_status in ("successful", "success"):
#             if payment.status != "paid_verified":
#                 payment.status = "paid_verified"
#                 payment.paid_at = timezone.now()
#                 # Safely compute expiry days
#                 days = payment.plan.duration_days if (payment.plan and getattr(payment.plan, 'duration_days', None) is not None) else 0
#                 payment.expires_at = timezone.now().date() + timedelta(days=days)
#                 payment.save()

#                 # Update tenant's paid_until date
#                 tenant = payment.tenant
#                 tenant.paid_until = payment.expires_at
#                 tenant.grace_until = tenant.paid_until + timedelta(days=3)  # 3 days grace period
#                 tenant.on_trial = False
#                 tenant.save()

#         return Response({"detail": "Payment verified successfully"}, status=status.HTTP_200_OK)