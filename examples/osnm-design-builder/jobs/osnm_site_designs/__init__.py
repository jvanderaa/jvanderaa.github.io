"""Executable Design Builder designs based on OSNM chapter 3's enterprise topology."""
from nautobot.apps.jobs import BooleanVar, ChoiceVar, IntegerVar, StringVar, register_jobs
from django.core.exceptions import ValidationError
from nautobot.dcim.models import Device, Interface, Location
from nautobot_design_builder.choices import DesignModeChoices
from nautobot_design_builder.context import Context
from nautobot_design_builder.contrib.ext import CableConnectionExtension
from nautobot_design_builder.design_job import DesignJob
from nautobot_design_builder.errors import DesignValidationError


def make_devices(specs, links, local_names):
    """Order cable creation on the later endpoint so both terminations exist."""
    devices = []
    order = {spec[0]: i for i, spec in enumerate(specs)}
    for name, role, ports, position in specs:
        interfaces = []
        for p in range(1, ports + 1):
            port = f"Ethernet{p}" if role != "Endpoint" else f"eth{p}"
            entry = {"name": port}
            for i, (a, ap, b, bp) in enumerate(links, 1):
                if name == b and port == bp and (a not in local_names or order[a] < order[b]):
                    entry["peer"] = {"device": a, "port": ap, "label": f"OSNM-{a}-{ap}-{b}-{bp}"}
                elif name == a and port == ap and (b not in local_names or order[b] < order[a]):
                    entry["peer"] = {"device": b, "port": bp, "label": f"OSNM-{a}-{ap}-{b}-{bp}"}
            interfaces.append(entry)
        devices.append({"name": name, "role": role, "interfaces": interfaces, "position": position})
    return devices


class DataCenterContext(Context):
    @property
    def location_name(self):
        return "DC1"

    @property
    def location_type(self):
        return "Datacenter"

    @property
    def rack_units(self):
        return 12

    @property
    def devices(self):
        specs = [
            ("spine-01", "Spine", 3, 1), ("spine-02", "Spine", 2, 2),
            ("leaf-01", "Leaf", 3, 3), ("leaf-02", "Leaf", 3, 4),
            ("wan-rtr", "WAN", 3, 5),
            ("dc-pc-01", "Endpoint", 1, None), ("dc-pc-02", "Endpoint", 1, None),
        ]
        links = [
            ("spine-01", "Ethernet1", "leaf-01", "Ethernet1"),
            ("spine-01", "Ethernet2", "leaf-02", "Ethernet1"),
            ("spine-02", "Ethernet1", "leaf-01", "Ethernet2"),
            ("spine-02", "Ethernet2", "leaf-02", "Ethernet2"),
            ("leaf-01", "Ethernet3", "dc-pc-01", "eth1"),
            ("leaf-02", "Ethernet3", "dc-pc-02", "eth1"),
            ("spine-01", "Ethernet3", "wan-rtr", "Ethernet1"),
        ]
        return make_devices(specs, links, {s[0] for s in specs})


class BranchContext(Context):
    @property
    def site_address(self):
        address = (self.get("physical_address") or "").strip()
        if address:
            return address
        try:
            return Location.objects.get(
                name=self["site_name"], location_type__name="Branch"
            ).physical_address.strip()
        except Location.DoesNotExist:
            return ""

    def validate_physical_address(self):
        if not self.site_address:
            raise DesignValidationError("Enter a physical address for a new site or a location without an address.")

    @property
    def location_name(self):
        return self["site_name"]

    @property
    def location_type(self):
        return "Branch"

    @property
    def devices(self):
        site = self["site_name"]
        specs = [(f"{site}-rtr", "Edge", 2, 1), (f"{site}-sw", "Access", self["access_ports"], 2)]
        links = [("wan-rtr", self["wan_port"], f"{site}-rtr", "Ethernet1"),
                 (f"{site}-rtr", "Ethernet2", f"{site}-sw", "Ethernet1")]
        if self["include_endpoint"]:
            specs.append((f"{site}-pc", "Endpoint", 1, None))
            links.append((f"{site}-sw", "Ethernet2", f"{site}-pc", "eth1"))
        return make_devices(specs, links, {s[0] for s in specs})

    def validate_site_pattern(self):
        if self["rack_units"] < 2:
            raise DesignValidationError("The branch pattern needs at least 2U for its router and switch.")
        if self["access_ports"] not in (2, 8, 24, 48):
            raise DesignValidationError("Choose an approved access-port pattern: 2, 8, 24 or 48.")
        if self["include_endpoint"] and self["access_ports"] < 2:
            raise DesignValidationError("The endpoint pattern requires an uplink and a host port.")
        if not Device.objects.filter(name="wan-rtr").exists():
            raise DesignValidationError("Run the OSNM Data Center Fabric design first to create wan-rtr.")
        interface = Interface.objects.get(device__name="wan-rtr", name=self["wan_port"])
        if interface.cable_id:
            expected_label = f"wan-rtr-{self['wan_port']}-{self['site_name']}-rtr-Ethernet1"
            if interface.cable.label != f"OSNM-{expected_label}":
                raise DesignValidationError(f"wan-rtr {self['wan_port']} is already connected to another site.")


class OSNMDataCenter(DesignJob):
    """Build OSNM's two-spine/two-leaf fabric and WAN hub as source-of-truth objects."""
    class Meta:
        name = "OSNM Data Center Fabric"
        description = "Create DC1: two spines, two leaves, WAN hub and two endpoints from the OSNM enterprise lab."
        design_mode = DesignModeChoices.DEPLOYMENT
        context_class = DataCenterContext
        design_file = "templates/site.yaml.j2"
        report = "templates/report.md.j2"
        extensions = [CableConnectionExtension]
        dryrun_default = True
        has_sensitive_variables = False
        version = "1.0.0"
        docs = """## OSNM enterprise lab / data center

Create **DC1**, rack **DC1-R01**, and the exact connected devices from chapter 3:
`spine-01`, `spine-02`, `leaf-01`, `leaf-02`, `wan-rtr`, `dc-pc-01`, `dc-pc-02`.

The design creates planned inventory, interfaces and seven cables. Branch uplinks
are reserved on `wan-rtr` Ethernet2 and Ethernet3. Run **Dry run** first to validate
the database changes, then disable dry run to create the deployment.

This lab changes Nautobot records only. It does not deploy Containerlab or send device configuration.
"""


class OSNMBranchSite(DesignJob):
    """Repeat the book's router-switch-endpoint site pattern with a few inputs."""
    site_name = StringVar(label="Site name", default="site1", regex=r"^site[1-9][0-9]*$", description="OSNM branch identifier, for example site1 or site2.")
    physical_address = StringVar(
        label="Physical address", required=False, max_length=200,
        description="Required for a new site. Leave blank to reuse the existing Location address.",
    )
    wan_port = ChoiceVar(label="WAN hub port", choices=(("Ethernet2", "Ethernet2 · site1"), ("Ethernet3", "Ethernet3 · site2")), default="Ethernet2")
    access_ports = IntegerVar(label="Access switch ports", default=2, min_value=2, max_value=48, description="Approved patterns: 2 (exact OSNM lab), 8, 24 or 48.")
    rack_units = IntegerVar(label="Rack height (U)", default=6, min_value=1, max_value=42, description="The branch router and switch require 2U in this illustrative placement.")
    include_endpoint = BooleanVar(label="Include lab endpoint", default=True, description="Create the Alpine PC record and its cable, matching OSNM chapter 3.")

    @classmethod
    def as_form_class(cls):
        """Present context validation as form errors in the pinned DB 3.1.2 release."""
        form_class = super().as_form_class()
        original_clean = form_class.clean

        def clean(form):
            try:
                return original_clean(form)
            except DesignValidationError as error:
                raise ValidationError(str(error)) from error

        form_class.clean = clean
        return form_class

    class Meta:
        name = "OSNM Branch Site"
        description = "Repeatable branch design: location, rack, router, access switch, optional endpoint and labeled cabling."
        design_mode = DesignModeChoices.DEPLOYMENT
        context_class = BranchContext
        design_file = "templates/site.yaml.j2"
        report = "templates/report.md.j2"
        extensions = [CableConnectionExtension]
        dryrun_default = True
        has_sensitive_variables = False
        version = "1.0.0"
        docs = """## One pattern, two sites

Use `site1` with **wan-rtr Ethernet2**, then `site2` with **Ethernet3**.
With two access ports and the endpoint enabled, the device names and connections
match the enterprise topology in OSNM chapter 3.

Every deployment creates a Branch location, a rack, `<site>-rtr`, `<site>-sw`,
an optional `<site>-pc`, interfaces and labeled cables. Reference catalog objects
are pre-seeded. Deployments track ownership and subsequent design changes.

Use dry run to validate without retaining inventory changes. The database JobResult
and logs remain as evidence. This is a local demonstration using synthetic records;
no real network devices are contacted or configured.
"""


name = "OSNM Site Designs"
register_jobs(OSNMDataCenter, OSNMBranchSite)
