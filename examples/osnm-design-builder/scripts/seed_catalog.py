"""Seed only reference catalog data into this new isolated screenshot database."""
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device, DeviceType, Interface, Location, LocationType, Manufacturer, Platform, Rack, Cable
from nautobot.extras.models import Role, Status

cts = [ContentType.objects.get_for_model(m) for m in (Device, Interface, Location, Rack, Cable)]
planned, _ = Status.objects.get_or_create(name="Planned", defaults={"color": "00bcd4"})
planned.content_types.add(*cts)
for name, color in [("Spine", "3f51b5"), ("Leaf", "2196f3"), ("WAN", "9c27b0"), ("Edge", "ff9800"), ("Access", "4caf50"), ("Endpoint", "607d8b")]:
    role, _ = Role.objects.get_or_create(name=name, defaults={"color": color})
    role.content_types.add(ContentType.objects.get_for_model(Device))
for name in ("Branch", "Datacenter"):
    lt, _ = LocationType.objects.get_or_create(name=name)
    lt.content_types.add(*[ContentType.objects.get_for_model(m) for m in (Device, Rack)])
arista, _ = Manufacturer.objects.get_or_create(name="Arista")
linux, _ = Manufacturer.objects.get_or_create(name="Linux")
DeviceType.objects.get_or_create(model="cEOS lab node", manufacturer=arista, defaults={"u_height": 1, "is_full_depth": False})
DeviceType.objects.get_or_create(model="Alpine lab endpoint", manufacturer=linux, defaults={"u_height": 0, "is_full_depth": False})
Platform.objects.get_or_create(name="Arista EOS", defaults={"manufacturer": arista, "network_driver": "arista_eos"})
print("Seeded OSNM reference catalog. No locations, devices or cables pre-created.")
