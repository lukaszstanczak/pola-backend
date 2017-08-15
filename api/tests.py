# coding=utf-8
from mock import patch
from test_plus.test import TestCase
from django.core.cache import cache
from company.factories import CompanyFactory
from pola.models import Query
from product.factories import ProductFactory


class add_ai_picsTestCase(TestCase):
    url = '/a/v3/add_ai_pics'


class get_by_code_v3TestCase(TestCase):
    url = '/a/v3/get_by_code'


class create_report_v3TestCase(TestCase):
    url = '/a/v3/create_report'


class get_by_code_v2TestCase(TestCase):
    url = '/a/v2/get_by_code'


class create_report_v2TestCase(TestCase):
    url = '/a/v2/create_report'


class update_report_v2TestCase(TestCase):
    url = '/a/v2/update_report'


class attach_file_v2TestCase(TestCase):
    url = '/a/v2/attach_file'


class get_by_codeTestCase(TestCase):
    code = "5901887005100"
    url_pattern = '/a/get_by_code/%s'
    url = url_pattern % code

    def setUp(self):
        super(get_by_codeTestCase, self).setUp()
        cache.clear()

    @patch('pola.logic.get_by_code')
    def test_not_found_product(self, get_by_code_mock):
        product = ProductFactory(code=self.code, company=None);
        get_by_code_mock.return_value = product
        resp = self.client.get(self.url, {'device_id': 123})

        self.assertEqual(resp.json(), {
            'report': 'ask_for_company',
            'code': product.code,
            'verified': False,
            'plScore': None,
            'id': product.pk
        })

    @patch('pola.logic.get_by_code')
    def test_rate_limit(self, get_by_code_mock):
        get_by_code_mock.return_value = ProductFactory(code=self.code, company=None)
        for _ in range(2):
            resp = self.client.get(self.url, {'device_id': 123})
            self.assertEqual(resp.status_code, 200)

        resp = self.client.get(self.url, {'device_id': 123})
        self.assertEqual(resp.status_code, 403)

    @patch('pola.logic.get_by_code')
    def test_increment_product_query_counter(self, get_by_code_mock):
        p = ProductFactory(code=self.code, company=None)
        get_by_code_mock.return_value = p
        self.assertEqual(p.query_count, 0)
        self.client.get(self.url, {'device_id': 123})
        p.refresh_from_db();
        self.assertEqual(p.query_count, 1)
        self.client.get(self.url, {'device_id': 123})
        p.refresh_from_db();
        self.assertEqual(p.query_count, 2)

    @patch('pola.logic.get_by_code')
    def test_increment_company_query_counter(self, get_by_code_mock):
        c = CompanyFactory()
        p = ProductFactory(code=self.code, company=c)
        get_by_code_mock.return_value = p

        self.assertEqual(c.query_count, 0)
        self.client.get(self.url, {'device_id': 123})

        c.refresh_from_db();
        self.assertEqual(c.query_count, 1)

        self.client.get(self.url, {'device_id': 123})

        c.refresh_from_db();
        self.assertEqual(c.query_count, 2)

    @patch('pola.logic.get_by_code')
    def test_save_query(self, get_by_code_mock):
        p = ProductFactory(code=self.code)
        get_by_code_mock.return_value = p

        self.client.get(self.url, {'device_id': 123})
        query = Query.objects.latest()

        self.assertEqual(query.product_id, p.pk)
        self.assertEqual(query.client, '123')
        self.assertEqual(query.was_590, True)

    @patch('pola.logic.get_by_code')
    def test_save_query_not_590(self, get_by_code_mock):
        p = ProductFactory(code="1231887005100")
        get_by_code_mock.return_value = p

        self.client.get(self.url_pattern % p.code, {'device_id': 123})

        query = Query.objects.latest()
        self.assertEqual(query.was_590, False)


class create_reportTestCase(TestCase):
    url = '/a/create_report'


class update_reportTestCase(TestCase):
    url = '/a/update_report'


class attach_fileTestCase(TestCase):
    url = '/a/attach_file'

