from networkapi.api_rest import exceptions as api_exceptions
from networkapi.plugins import exceptions as base_exceptions
import logging
from ..base import BasePlugin
import json
import bigsuds
import itertools


from networkapi.plugins.F5 import lb, pool, poolmember, util, monitor

log = logging.getLogger(__name__)


class Generic(BasePlugin):

    #######################################
    # POOLMEMBER
    #######################################
    @util.transation
    def setStateMember(self, pools):

        pls = util._trataParam(pools)

        plm = poolmember.PoolMember(self._lb)

        plm.setStates(
            names=pls['pools_names'],
            members=pls['pools_members']['members'],
            monitor_state=pls['pools_members']['monitor'],
            session_state=pls['pools_members']['session'])

    @util.transation
    def setConnectionLimitMember(self, pools):

        pls = util._trataParam(pools)

        plm = poolmember.PoolMember(self._lb)
        plm.setConnectionLimit(
            names=pls['pools_names'],
            members=pls['pools_members']['members'],
            connection_limit=pls['pools_members']['limit'])

    @util.transation
    def setPriorityMember(self, pools):

        pls = util._trataParam(pools)

        plm = poolmember.PoolMember(self._lb)
        plm.setPriority(
            names=pls['pools_names'],
            members=pls['pools_members']['members'],
            priority=pls['pools_members']['priority'])

    @util.transation
    def getStateMember(self, pools):
        pls = util._trataParam(pools)

        plm = poolmember.PoolMember(self._lb)
        return plm.getStates(
            names=pls['pools_names'],
            members=pls['pools_members']['members'])

    @util.transation
    def createMember(self, pools):

        pls = util._trataParam(pools)

        plm = poolmember.PoolMember(self._lb)
        return plm.create(
            names=pls['pools_names'],
            members=pls['pools_members']['members'])

    @util.transation
    def removeMember(self, pools):

        pls = util._trataParam(pools)

        plm = poolmember.PoolMember(self._lb)
        return plm.remove(
            names=pls['pools_names'],
            members=pls['pools_members']['members'])

    #######################################
    # POOL
    #######################################
    @util.connection
    def createPool(self, pools):

        monitor_associations = []
        pls = util._trataParam(pools)

        mon = monitor.Monitor(self._lb)

        monitor_associations = mon.createTemplate(
            names=pls['pools_names'],
            healthcheck=pls['pools_healthcheck']
        )

        try:
            self._lb._channel.System.Session.start_transaction()

            pl = pool.Pool(self._lb)

            pl.create(
                names=pls['pools_names'],
                lbmethod=pls['pools_lbmethod'],
                members=pls['pools_members']['members'])

            pl.setMonitorAssociation(monitor_associations=monitor_associations)

            pl.setServiceDownAction(
                names=pls['pools_names'],
                actions=pls['pools_actions'])

            plm = poolmember.PoolMember(self._lb)

            plm.setConnectionLimit(
                names=pls['pools_names'],
                members=pls['pools_members']['members'],
                connection_limit=pls['pools_members']['limit'])

            plm.setPriority(
                names=pls['pools_names'],
                members=pls['pools_members']['members'],
                priority=pls['pools_members']['priority'])

            plm.setStates(
                names=pls['pools_names'],
                members=pls['pools_members']['members'],
                monitor_state=pls['pools_members']['monitor'],
                session_state=pls['pools_members']['session'])

        except Exception, e:
            self._lb._channel.System.Session.rollback_transaction()
            if monitor_associations != []:
                template_names = [m['monitor_rule']['monitor_templates'] for m in monitor_associations]
                mon.deleteTemplate(
                    template_names=template_names
                )
            raise base_exceptions.CommandErrorException(e)
        else:
            self._lb._channel.System.Session.submit_transaction()

    @util.connection
    def updatePool(self, pools):

        monitor_associations = []
        pls = util._trataParam(pools)

        pl = pool.Pool(self._lb)
        mon = monitor.Monitor(self._lb)

        mon.deleteTemplateAssoc(names=pls['pools_names'])

        monitor_associations = mon.createTemplate(
            names=pls['pools_names'],
            healthcheck=pls['pools_healthcheck']
        )

        try:
            self._lb._channel.System.Session.start_transaction()

            pl.setMonitorAssociation(monitor_associations=monitor_associations)

            pl.setLbMethod(
                names=pls['pools_names'],
                lbmethod=pls['pools_lbmethod'])

            pl.setServiceDownAction(
                names=pls['pools_names'],
                actions=pls['pools_actions'])

            plm = poolmember.PoolMember(self._lb)
            

            if pls['pools_members']['members_remove']:
                plm.remove(
                    names=pls['pools_names'],
                    members=pls['pools_members']['members_remove'])
                
            if pls['pools_members']['members_new']:
                plm.create(
                    names=pls['pools_names'],
                    members=pls['pools_members']['members_new'])

            plm.setConnectionLimit(
                names=pls['pools_names'],
                members=pls['pools_members']['members'],
                connection_limit=pls['pools_members']['limit'])

            plm.setPriority(
                names=pls['pools_names'],
                members=pls['pools_members']['members'],
                priority=pls['pools_members']['priority'])

            plm.setStates(
                names=pls['pools_names'],
                members=pls['pools_members']['members'],
                monitor_state=pls['pools_members']['monitor'],
                session_state=pls['pools_members']['session'])

        except Exception, e:
            self._lb._channel.System.Session.rollback_transaction()
            if monitor_associations != []:
                template_names = [m for m in list(itertools.chain(*[m['monitor_rule']['monitor_templates'] for m in monitor_associations])) if 'MONITOR' in m]
                if template_names:
                    mon.deleteTemplate(
                        template_names=template_names
                    )
            raise base_exceptions.CommandErrorException(e)
        else:
            self._lb._channel.System.Session.submit_transaction()

    @util.connection
    def deletePool(self, pools):

        pls = util._trataParam(pools)

        pl = pool.Pool(self._lb)
        mon = monitor.Monitor(self._lb)

        mon.deleteTemplateAssoc(names=pls['pools_names'])
        pl.delete(names=pls['pools_names'])
