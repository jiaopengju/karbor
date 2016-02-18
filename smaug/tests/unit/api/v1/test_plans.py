#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import mock
from oslo_config import cfg
from webob import exc

from smaug.api.v1 import plans
from smaug import context
from smaug import exception
from smaug.tests import base
from smaug.tests.unit.api import fakes

CONF = cfg.CONF

DEFAULT_NAME = 'My 3 tier application'
DEFAULT_PROVIDER_ID = 'efc6a88b-9096-4bb6-8634-cda182a6e12a'
DEFAULT_STATUS = 'suspended'
DEFAULT_PROJECT_ID = '39bb894794b741e982bd26144d2949f6'
DEFAULT_RESOURCES = [{'id': 'key1',
                      "type": "value1"}]


class PlanApiTest(base.TestCase):
    def setUp(self):
        super(PlanApiTest, self).setUp()
        self.controller = plans.PlansController()
        self.ctxt = context.RequestContext('admin', 'fakeproject', True)

    @mock.patch(
        'smaug.objects.plan.Plan.create')
    def test_plan_create(self, mock_plan_create):
        plan = self._plan_in_request_body()
        body = {"plan": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.controller.create(req, body)
        self.assertTrue(mock_plan_create.called)

    def test_plan_create_InvalidBody(self):
        plan = self._plan_in_request_body()
        body = {"planxx": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.assertRaises(exc.HTTPUnprocessableEntity, self.controller.create,
                          req, body)

    def test_plan_create_InvalidProviderId(self):
        plan = self._plan_in_request_body(name=DEFAULT_NAME,
                                          provider_id="",
                                          status=DEFAULT_STATUS,
                                          project_id=DEFAULT_PROJECT_ID,
                                          resources=[])
        body = {"plan": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.assertRaises(exception.InvalidInput, self.controller.create,
                          req, body)

    def test_plan_create_InvalidResources(self):
        plan = self._plan_in_request_body(name=DEFAULT_NAME,
                                          provider_id=DEFAULT_PROVIDER_ID,
                                          status=DEFAULT_STATUS,
                                          project_id=DEFAULT_PROJECT_ID,
                                          resources=[])
        body = {"plan": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.assertRaises(exception.InvalidInput, self.controller.create,
                          req, body)

    @mock.patch(
        'smaug.api.v1.plans.PlansController._plan_get')
    @mock.patch(
        'smaug.api.v1.plans.PlansController._plan_update')
    def test_plan_update(self, mock_plan_update, mock_plan_get):
        plan = self._plan_in_request_body()
        body = {"plan": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.controller.\
            update(req, "2a9ce1f3-cc1a-4516-9435-0ebb13caa398", body)
        self.assertTrue(mock_plan_update.called)
        self.assertTrue(mock_plan_get.called)

    def test_plan_update_InvalidBody(self):
        plan = self._plan_in_request_body()
        body = {"planxx": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.assertRaises(
            exc.HTTPBadRequest, self.controller.update,
            req, "2a9ce1f3-cc1a-4516-9435-0ebb13caa398", body)

    def test_plan_update_InvalidId(self):
        plan = self._plan_in_request_body()
        body = {"plan": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.assertRaises(
            exc.HTTPNotFound, self.controller.update,
            req, "2a9ce1f3-cc1a-4516-9435-0ebb13caa398", body)

    def test_plan_update_InvalidResources(self):
        plan = self._plan_in_request_body(name=DEFAULT_NAME,
                                          provider_id=DEFAULT_PROVIDER_ID,
                                          status=DEFAULT_STATUS,
                                          project_id=DEFAULT_PROJECT_ID,
                                          resources=[{'key1': 'value1'}])
        body = {"plan": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.assertRaises(
            exception.InvalidInput, self.controller.update,
            req, "2a9ce1f3-cc1a-4516-9435-0ebb13caa398", body)

    @mock.patch(
        'smaug.api.v1.plans.PlansController._get_all')
    def test_plan_list_detail(self, moak_get_all):
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.controller.index(req)
        self.assertTrue(moak_get_all.called)

    @mock.patch(
        'smaug.api.v1.plans.PlansController._plan_get')
    def test_plan_show(self, moak_plan_get):
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.controller.\
            show(req, '2a9ce1f3-cc1a-4516-9435-0ebb13caa398')
        self.assertTrue(moak_plan_get.called)

    def test_plan_show_Invalid(self):
        req = fakes.HTTPRequest.blank('/v1/plans/1')
        self.assertRaises(
            exc.HTTPBadRequest, self.controller.show,
            req, "1")

    @mock.patch(
        'smaug.api.v1.plans.PlansController._plan_get')
    def test_plan_delete(self, moak_plan_get):
        req = fakes.HTTPRequest.blank('/v1/plans')
        self.controller.\
            show(req, '2a9ce1f3-cc1a-4516-9435-0ebb13caa398')
        self.assertTrue(moak_plan_get.called)

    def test_plan_delete_Invalid(self):
        req = fakes.HTTPRequest.blank('/v1/plans/1')
        self.assertRaises(
            exc.HTTPBadRequest, self.controller.show,
            req, "1")

    @mock.patch(
        'smaug.api.v1.plans.check_policy')
    @mock.patch(
        'smaug.api.v1.plans.PlansController._plan_get')
    def test_plan_update_InvalidStatus(self, mock_plan_get, mock_check_policy):
        plan = self._plan_in_request_body(name=DEFAULT_NAME,
                                          provider_id=DEFAULT_PROVIDER_ID,
                                          status="started",
                                          project_id=DEFAULT_PROJECT_ID,
                                          resources=DEFAULT_RESOURCES)
        body = {"plan": plan}
        req = fakes.HTTPRequest.blank('/v1/plans')
        mock_plan_get.return_value = plan
        self.assertRaises(exception.InvalidPlan,
                          self.controller.update, req,
                          "2a9ce1f3-cc1a-4516-9435-0ebb13caa398",
                          body)

    def _plan_in_request_body(self, name=DEFAULT_NAME,
                              provider_id=DEFAULT_PROVIDER_ID,
                              status=DEFAULT_STATUS,
                              project_id=DEFAULT_PROJECT_ID,
                              resources=DEFAULT_RESOURCES):
        plan_req = {
            'name': name,
            'provider_id': provider_id,
            'status': status,
            'project_id': project_id,
            'resources': resources,
        }

        return plan_req