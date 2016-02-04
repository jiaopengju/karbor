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

"""Defines interface for DB access.

Functions in this module are imported into the smaug.db namespace. Call these
functions from smaug.db namespace, not the smaug.db.api namespace.

All functions in this module return objects that implement a dictionary-like
interface. Currently, many of these objects are sqlalchemy objects that
implement a dictionary interface. However, a future goal is to have all of
these objects be simple dictionaries.


**Related Flags**

:connection:  string specifying the sqlalchemy connection to use, like:
              `sqlite:///var/lib/smaug/smaug.sqlite`.

:enable_new_services:  when adding a new service to the database, is it in the
                       pool of available hardware (Default: True)

"""

from oslo_config import cfg
from oslo_db import concurrency as db_concurrency
from oslo_db import options as db_options


db_opts = [
    cfg.BoolOpt('enable_new_services',
                default=True,
                help='Services to be added to the available pool on create'),
]


CONF = cfg.CONF
CONF.register_opts(db_opts)
db_options.set_defaults(CONF)
CONF.set_default('sqlite_db', 'smaug.sqlite', group='database')

_BACKEND_MAPPING = {'sqlalchemy': 'smaug.db.sqlalchemy.api'}


IMPL = db_concurrency.TpoolDbapiWrapper(CONF, _BACKEND_MAPPING)

# The maximum value a signed INT type may have
MAX_INT = 0x7FFFFFFF


###################

def dispose_engine():
    """Force the engine to establish new connections."""

    # FIXME(jdg): When using sqlite if we do the dispose
    # we seem to lose our DB here.  Adding this check
    # means we don't do the dispose, but we keep our sqlite DB
    # This likely isn't the best way to handle this

    if 'sqlite' not in IMPL.get_engine().name:
        return IMPL.dispose_engine()
    else:
        return


###################


def service_destroy(context, service_id):
    """Destroy the service or raise if it does not exist."""
    return IMPL.service_destroy(context, service_id)


def service_get(context, service_id):
    """Get a service or raise if it does not exist."""
    return IMPL.service_get(context, service_id)


def service_get_by_host_and_topic(context, host, topic):
    """Get a service by host it's on and topic it listens to."""
    return IMPL.service_get_by_host_and_topic(context, host, topic)


def service_get_all(context, disabled=None):
    """Get all services."""
    return IMPL.service_get_all(context, disabled)


def service_get_all_by_topic(context, topic, disabled=None):
    """Get all services for a given topic."""
    return IMPL.service_get_all_by_topic(context, topic, disabled=disabled)


def service_get_by_args(context, host, binary):
    """Get the state of an service by node name and binary."""
    return IMPL.service_get_by_args(context, host, binary)


def service_create(context, values):
    """Create a service from the values dictionary."""
    return IMPL.service_create(context, values)


def service_update(context, service_id, values):
    """Set the given properties on an service and update it.

    Raises NotFound if service does not exist.

    """
    return IMPL.service_update(context, service_id, values)


def get_by_id(context, model, id, *args, **kwargs):
    return IMPL.get_by_id(context, model, id, *args, **kwargs)


###################


def trigger_get(context, id):
    """Get a trigger by its id.

    :param context: The security context
    :param id: ID of the trigger

    :returns: Dictionary-like object containing properties of the trigger

    Raises TriggerNotFound if trigger with the given ID doesn't exist.
    """
    return IMPL.trigger_get(context, id)


def trigger_create(context, values):
    """Create a trigger from the values dictionary.

    :param context: The security context
    :param values: Dictionary containing trigger properties

    :returns: Dictionary-like object containing the properties of the created
              trigger
    """
    return IMPL.trigger_create(context, values)


def trigger_update(context, id, values):
    """Set the given properties on a trigger and update it.

    :param context: The security context
    :param id: ID of the trigger
    :param values: Dictionary containing trigger properties to be updated

    :returns: Dictionary-like object containing the properties of the updated
              trigger

    Raises TriggerNotFound if trigger with the given ID doesn't exist.
    """
    return IMPL.trigger_update(context, id, values)


def trigger_delete(context, id):
    """Delete a trigger from the database.

    :param context: The security context
    :param id: ID of the trigger

    Raises TriggerNotFound if trigger with the given ID doesn't exist.
    """
    return IMPL.trigger_delete(context, id)


###################


def scheduled_operation_state_get(context, operation_id):
    """Get a scheduled operation state by its id.

    :param context: The security context
    :param operation_id: Operation_id of the scheduled operation state

    :returns: Dictionary-like object containing properties of the scheduled
     operation state

    Raises ScheduledOperationStateNotFound if scheduled operation state with
     the given ID doesn't exist.
    """
    return IMPL.scheduled_operation_state_get(context, operation_id)


def scheduled_operation_state_create(context, values):
    """Create a scheduled operation state from the values dictionary.

    :param context: The security context
    :param values: Dictionary containing scheduled operation state properties

    :returns: Dictionary-like object containing the properties of the created
              scheduled operation state
    """
    return IMPL.scheduled_operation_state_create(context, values)


def scheduled_operation_state_update(context, operation_id, values):
    """Set the given properties on a scheduled operation state and update it.

    :param context: The security context
    :param operation_id: Operation_id of the scheduled operation state
    :param values: Dictionary containing scheduled operation state properties
                   to be updated

    :returns: Dictionary-like object containing the properties of the updated
              scheduled operation state

    Raises ScheduledOperationStateNotFound if scheduled operation state with
    the given ID doesn't exist.
    """
    return IMPL.scheduled_operation_state_update(context, operation_id, values)


def scheduled_operation_state_delete(context, operation_id):
    """Delete a scheduled operation state from the database.

    :param context: The security context
    :param operation_id: Operation_id of the scheduled operation state

    Raises ScheduledOperationStateNotFound if scheduled operation state with
    the given ID doesn't exist.
    """
    return IMPL.scheduled_operation_state_delete(context, operation_id)


###################


def scheduled_operation_log_get(context, log_id):
    """Get a scheduled operation log by its id.

    :param context: The security context
    :param log_id: Log_id of the scheduled operation log

    :returns: Dictionary-like object containing properties of the scheduled
     operation log

    Raises ScheduledOperationLogNotFound if scheduled operation log with
     the given ID doesn't exist.
    """
    return IMPL.scheduled_operation_log_get(context, log_id)


def scheduled_operation_log_create(context, values):
    """Create a scheduled operation log from the values dictionary.

    :param context: The security context
    :param values: Dictionary containing scheduled operation log properties

    :returns: Dictionary-like object containing the properties of the created
              scheduled operation log
    """
    return IMPL.scheduled_operation_log_create(context, values)


def scheduled_operation_log_update(context, log_id, values):
    """Set the given properties on a scheduled operation log and update it.

    :param context: The security context
    :param log_id: Log_id of the scheduled operation log
    :param values: Dictionary containing scheduled operation log properties
                   to be updated

    :returns: Dictionary-like object containing the properties of the updated
              scheduled operation log

    Raises ScheduledOperationLogNotFound if scheduled operation log with
    the given ID doesn't exist.
    """
    return IMPL.scheduled_operation_log_update(context, log_id, values)


def scheduled_operation_log_delete(context, log_id):
    """Delete a scheduled operation log from the database.

    :param context: The security context
    :param log_id: Log_id of the scheduled operation log

    Raises ScheduledOperationLogNotFound if scheduled operation log with
    the given ID doesn't exist.
    """
    return IMPL.scheduled_operation_log_delete(context, log_id)


def plan_get(context, plan_id):
    """Get a plan or raise if it does not exist."""
    return IMPL.plan_get(context, plan_id)


def plan_create(context, values):
    """Create a plan from the values dictionary."""
    return IMPL.plan_create(context, values)


def plan_update(context, plan_id, values):
    """Set the given properties on a plan and update it.

    Raises NotFound if plan does not exist.

    """
    return IMPL.plan_update(context, plan_id, values)


def plan_resources_update(context, plan_id, resources):
    """Update resources if it exists, otherwise create it."""
    return IMPL.plan_resources_update(context, plan_id, resources)


def plan_destroy(context, plan_id):
    """Destroy the plan or raise if it does not exist."""
    return IMPL.plan_destroy(context, plan_id)


def plan_get_all(context, marker, limit, sort_keys=None, sort_dirs=None,
                 filters=None, offset=None):
    """Get all plans."""
    return IMPL.plan_get_all(context, marker, limit, sort_keys=sort_keys,
                             sort_dirs=sort_dirs, filters=filters,
                             offset=offset)
