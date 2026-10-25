"""Run inside the seeded lab: nautobot-server shell < scripts/test_address.py."""
import unittest
import sys
from django.conf import settings
from django.db import transaction
from nautobot.dcim.models import Location, LocationType
from nautobot.extras.models import Status
from pathlib import Path
from nautobot_design_builder.jinja2 import new_template_environment
import yaml
sys.path.insert(0, settings.JOBS_ROOT)
from osnm_site_designs import BranchContext, OSNMBranchSite


class PhysicalAddressTests(unittest.TestCase):
    def data(self, **overrides):
        return dict(deployment_name="osnm-site9", site_name="site9", wan_port="Ethernet3",
                    access_ports=2, rack_units=6, include_endpoint=True,
                    dryrun=True, import_mode=False, **overrides)

    def test_new_site_requires_a_nonblank_address(self):
        for address in ("", "   "):
            form = OSNMBranchSite.as_form_class()(data=self.data(physical_address=address))
            self.assertFalse(form.is_valid(), "New sites must not accept blank addresses")
            self.assertIn("physical address", str(form.errors).lower())

    def test_form_accepts_a_multiline_address(self):
        address = '100 Example Avenue\nSuite "A"\nChicago, IL 60601'
        form = OSNMBranchSite.as_form_class()(data=self.data(physical_address=address))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["physical_address"], address)

    def test_address_round_trips_through_the_yaml_template(self):
        address = '100 Example Avenue\nSuite "A": West\nChicago, IL 60601'
        context = BranchContext(data=self.data(physical_address=address))
        env = new_template_environment(context, base_dir=str(Path(settings.JOBS_ROOT)/'osnm_site_designs/templates'))
        rendered = env.get_template('site.yaml.j2').render()
        self.assertEqual(yaml.safe_load(rendered)["locations"][0]["physical_address"], address)

    def test_blank_input_reuses_an_existing_location_address(self):
        with transaction.atomic():
            Location.objects.create(name="site9", location_type=LocationType.objects.get(name="Branch"),
                                    status=Status.objects.get(name="Planned"),
                                    physical_address="100 Example Avenue, Chicago, IL 60601")
            context = BranchContext(data=self.data(physical_address=" "))
            self.assertEqual(context.site_address, "100 Example Avenue, Chicago, IL 60601")
            form = OSNMBranchSite.as_form_class()(data=self.data(physical_address=""))
            self.assertTrue(form.is_valid(), form.errors)
            transaction.set_rollback(True)


result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PhysicalAddressTests))
if not result.wasSuccessful():
    raise SystemExit(1)
