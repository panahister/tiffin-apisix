import importlib.util
import pathlib
import stat
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROFILE = ROOT / "product/tiffin-local"
TEMPLATE = (PROFILE / "apisix.template.yaml").read_text(encoding="utf-8")

SPEC = importlib.util.spec_from_file_location("render", ROOT / "scripts/render.py")
RENDER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RENDER)


class GatewayProfileTests(unittest.TestCase):
    def test_standalone_mode_has_no_admin_api_or_etcd(self):
        config = (PROFILE / "config.yaml").read_text(encoding="utf-8")
        self.assertIn("role: data_plane", config)
        self.assertIn("config_provider: yaml", config)
        self.assertNotIn("etcd:", config)
        self.assertNotIn("admin:", config)

    def test_public_and_protected_restaurant_routes_are_separate(self):
        self.assertIn("id: menus-browse", TEMPLATE)
        self.assertIn("methods: [GET]", TEMPLATE)
        self.assertIn("priority: 20", TEMPLATE)
        self.assertIn("limit-count:", TEMPLATE)
        self.assertIn('id: restaurants,   uri: "/v1/restaurants*"', TEMPLATE)
        self.assertIn("plugin_config_id: needs-a-token", TEMPLATE)

    def test_payments_has_no_public_upstream_or_route(self):
        non_comment = "\n".join(line for line in TEMPLATE.splitlines() if not line.lstrip().startswith("#"))
        self.assertNotIn("payments", non_comment.lower())

    def test_both_auth_profiles_preserve_backend_authority(self):
        off = (PROFILE / "edge-auth.off.yaml").read_text(encoding="utf-8")
        keycloak = (PROFILE / "edge-auth.keycloak.yaml").read_text(encoding="utf-8")
        self.assertIn("serverless-pre-function", off)
        self.assertIn("openid-connect", keycloak)
        self.assertIn("bearer_only: true", keycloak)
        self.assertIn("use_jwks: true", keycloak)
        self.assertIn("set_access_token_header: false", keycloak)
        self.assertIn("set_id_token_header: false", keycloak)
        self.assertIn("set_userinfo_header: false", keycloak)

    def test_renderer_resolves_markers_and_writes_owner_only_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            certificate = root / "localhost.crt"
            private_key = root / "localhost.key"
            output = root / "apisix.yaml"
            certificate.write_text("CERTIFICATE-LINE\n", encoding="utf-8")
            private_key.write_text("PRIVATE-KEY-LINE\n", encoding="utf-8")

            rendered = RENDER.render("keycloak", certificate, private_key)
            RENDER.write_private(output, rendered)

            self.assertNotIn("__EDGE_AUTH__", rendered)
            self.assertNotIn("__CERTIFICATE__", rendered)
            self.assertNotIn("__KEY__", rendered)
            self.assertIn("      CERTIFICATE-LINE", rendered)
            self.assertIn("      PRIVATE-KEY-LINE", rendered)
            self.assertIn("      openid-connect:", rendered)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)

    def test_public_documents_contain_no_persian_specific_letters(self):
        forbidden = set("پچژگک‌ی")
        candidates = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
        for path in candidates:
            self.assertFalse(forbidden.intersection(path.read_text(encoding="utf-8")), path)


if __name__ == "__main__":
    unittest.main()
