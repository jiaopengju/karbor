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

from datetime import datetime
from datetime import timedelta

from smaug.common import constants
from smaug import context
from smaug import objects
from smaug.services.operationengine.operations import base as base_operation
from smaug.tests import base


class OperationTestCase(base.TestCase):
    """Test cases for ProtectOperation class."""

    def setUp(self):
        super(OperationTestCase, self).setUp()
        self._operation_class = base_operation.Operation
        self._operation_db = self._create_operation()

    def test_run_execute(self):
        now = datetime.utcnow() - timedelta(hours=1)
        param = {
            'operation_id': self._operation_db.id,
            'triggered_time': now,
            'expect_start_time': now,
            'window_time': 30,
            'run_type': constants.OPERATION_RUN_TYPE_EXECUTE,
            'user_id': self._operation_db.user_id,
            'project_id': self._operation_db.project_id
        }
        self._operation_class.run(self._operation_db.operation_definition,
                                  param=param)

        logs = objects.ScheduledOperationLogList.get_by_filters(
            context.get_admin_context(),
            {'state': constants.OPERATION_EXE_STATE_DROPPED_OUT_OF_WINDOW,
             'operation_id': self._operation_db.id}, 1,
            None, ['created_at'], ['desc'])

        self.assertTrue(logs is not None)
        log = logs.objects[0]
        self.assertTrue(now, log.triggered_time)

    def test_run_resume(self):
        log = self._create_operation_log(self._operation_db.id)
        now = datetime.utcnow() - timedelta(hours=1)
        param = {
            'operation_id': self._operation_db.id,
            'triggered_time': now,
            'expect_start_time': now,
            'window_time': 30,
            'run_type': constants.OPERATION_RUN_TYPE_RESUME,
            'user_id': self._operation_db.user_id,
            'project_id': self._operation_db.project_id
        }
        self._operation_class.run(self._operation_db.operation_definition,
                                  param=param)

        logs = objects.ScheduledOperationLogList.get_by_filters(
            context.get_admin_context(),
            {'state': constants.OPERATION_EXE_STATE_DROPPED_OUT_OF_WINDOW,
             'operation_id': self._operation_db.id}, 1,
            None, ['created_at'], ['desc'])

        self.assertTrue(logs is not None)
        log1 = logs.objects[0]
        self.assertTrue(log.id, log1.id)

    def _create_operation(self):
        operation_info = {
            'name': 'protect vm',
            'description': 'protect vm resource',
            'operation_type': 'protect',
            'user_id': '123',
            'project_id': '123',
            'trigger_id': '123',
            'operation_definition': {
                'provider_id': '123',
                'plan_id': '123'
            }
        }
        operation = objects.ScheduledOperation(context.get_admin_context(),
                                               **operation_info)
        operation.create()
        return operation

    def _create_operation_log(self, operation_id):
        log_info = {
            'operation_id': operation_id,
            'state': constants.OPERATION_EXE_STATE_IN_PROGRESS,
        }
        log = objects.ScheduledOperationLog(context.get_admin_context(),
                                            **log_info)
        log.create()
        return log
