from datetime import datetime, timezone
from .authority_models import GovernedAuthority, GovernedApplicability
from .identifiers import IdentifierFactory

def _instant(value):
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError('Timezone-aware effective time required')
    return value.astimezone(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')

class AuthorityService:
    def __init__(self, repository, identifiers=None):
        self.repository, self.identifiers = repository, identifiers or IdentifierFactory()
        self._test_failure_hook = None
        self._test_supersession_failure_hook = None

    def create_authority(self, origin_locator, content_hash, context_revision_id, parameter_reference, effective_from, effective_until=None, authority_id=None, authority_version=1, actor_reference='system', reason='published'):
        if not origin_locator or not content_hash or not context_revision_id or not parameter_reference or not actor_reference or not reason:
            raise ValueError('Authority fields are required')
        start, end = _instant(effective_from), _instant(effective_until) if effective_until else None
        if end and end <= start: raise ValueError('Invalid authority interval')
        aid = authority_id or self.identifiers.new('authority')
        now = datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')
        with self.repository.transaction() as c:
            c.execute('INSERT INTO governed_authority VALUES (?,?,?,?,?)',(aid,authority_version,origin_locator,content_hash,now))
            c.execute('INSERT INTO authority_scope VALUES (?,?,?,?)',(aid,authority_version,context_revision_id,parameter_reference))
            c.execute('INSERT INTO authority_state VALUES (?,?,?,?,?)',(aid,authority_version,'PUBLISHED',now,None))
            c.execute('INSERT INTO authority_temporal_boundary VALUES (?,?,?,?)',(aid,authority_version,start,end))
            eid=self.identifiers.new('event'); c.execute('INSERT INTO authority_event VALUES (?,?,?,?,?,?,?,?,?)',(eid,aid,authority_version,'PUBLISHED',actor_reference,reason,None,None,now))
        return GovernedAuthority(aid,authority_version,origin_locator,content_hash,now,context_revision_id,parameter_reference,start,end,'PUBLISHED')

    def activate(self, authority_id, authority_version, actor_reference='system', reason='activated'):
        return self._transition(authority_id, authority_version, 'ACTIVE', actor_reference, reason)

    def create_applicability(self, authority_id, authority_version, context_revision_id,
                             parameter_reference, effective_from, actor_reference, reason):
        if not all((authority_id, context_revision_id, parameter_reference, actor_reference, reason)):
            raise ValueError('Applicability fields are required')
        start = _instant(effective_from)
        aid = self.identifiers.new('aps_applicability')
        now = datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')
        with self.repository.transaction() as c:
            if not c.execute('SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?',(authority_id,authority_version)).fetchone():
                raise ValueError('Unmapped authority')
            overlap = c.execute("SELECT 1 FROM authority_applicability_temporal WHERE context_revision_id=? AND parameter_reference=? AND effective_from<=? AND (terminal_effective_at IS NULL OR ? < terminal_effective_at)", (context_revision_id, parameter_reference, start, start)).fetchone()
            if overlap: raise ValueError('Applicability overlap blocked')
            c.execute('INSERT INTO authority_applicability VALUES (?,?,?,?,?,?,?)',(aid,authority_id,authority_version,context_revision_id,parameter_reference,start,now))
            c.execute('INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)',(self.identifiers.new('event'),aid,'PUBLISHED',start,now,actor_reference,reason,None))
        return GovernedApplicability(aid,authority_id,authority_version,context_revision_id,parameter_reference,start,now)

    def resolve_applicability(self, context_revision_id, parameter_reference, measured_at):
        instant = _instant(measured_at)
        with self.repository._optional_connection(None) as c:
            rows = c.execute("SELECT applicability_id,authority_id,authority_version,context_revision_id,parameter_reference,effective_from FROM authority_applicability_temporal WHERE context_revision_id=? AND parameter_reference=? AND effective_from<=? AND (terminal_effective_at IS NULL OR ?<terminal_effective_at)", (context_revision_id,parameter_reference,instant,instant)).fetchall()
        if len(rows) != 1: raise ValueError('Applicability resolution blocked')
        return GovernedApplicability(*rows[0], '')

    def revoke_applicability(self, applicability_id, effective_at, actor_reference, reason):
        return self._terminal_applicability(applicability_id,'REVOKED',effective_at,actor_reference,reason,None)

    def supersede_applicability(self, predecessor_id, authority_id, authority_version, context_revision_id, parameter_reference, effective_from, actor_reference, reason):
        if not all((authority_id, context_revision_id, parameter_reference, actor_reference, reason)):
            raise ValueError('Applicability fields are required')
        start = _instant(effective_from); now = datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')
        with self.repository.transaction() as c:
            pred=c.execute('SELECT authority_id,authority_version,context_revision_id,parameter_reference,effective_from FROM authority_applicability WHERE applicability_id=?',(predecessor_id,)).fetchone()
            if not pred: raise ValueError('Invalid predecessor or backdating')
            state=c.execute('SELECT state FROM authority_applicability_state WHERE applicability_id=?',(predecessor_id,)).fetchone()
            if not state or state[0] != 'ACTIVE': raise ValueError('Predecessor is not ACTIVE')
            if start < pred[4]: raise ValueError('Invalid predecessor or backdating')
            if not c.execute('SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?',(authority_id,authority_version)).fetchone(): raise ValueError('Unmapped authority')
            successor = self.identifiers.new('aps_applicability')
            predecessor_event = self.identifiers.new('event')
            successor_event = self.identifiers.new('event')
            c.execute('INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)',(predecessor_event,predecessor_id,'SUPERSEDED',start,now,actor_reference,reason,successor))
            if self._test_supersession_failure_hook is not None:
                self._test_supersession_failure_hook('after_predecessor_event')
            c.execute('INSERT INTO authority_applicability VALUES (?,?,?,?,?,?,?)',(successor,authority_id,authority_version,context_revision_id,parameter_reference,start,now))
            if self._test_supersession_failure_hook is not None:
                self._test_supersession_failure_hook('after_successor_applicability')
            c.execute('INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)',(successor_event,successor,'PUBLISHED',start,now,actor_reference,reason,None))
        return successor

    def _terminal_applicability(self, applicability_id, event_type, effective_at, actor_reference, reason, successor):
        at=_instant(effective_at); now=datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')
        with self.repository.transaction() as c:
            row=c.execute('SELECT effective_from,context_revision_id,parameter_reference,authority_id,authority_version FROM authority_applicability WHERE applicability_id=?',(applicability_id,)).fetchone()
            if not row or at < row[0] or not row[1] or not row[2]: raise ValueError('Invalid terminal time or applicability linkage')
            authority=c.execute('SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?',(row[3],row[4])).fetchone()
            if not authority: raise ValueError('Unmapped authority')
            affected=c.execute("SELECT 1 FROM governed_evaluation e JOIN governed_measurement m ON m.measurement_id=e.measurement_id WHERE m.context_revision_id=? AND m.parameter_reference=? AND m.measured_at>=? AND m.measured_at<? LIMIT 1",(row[1],row[2],row[0],at)).fetchone()
            if affected: raise ValueError('Retroactive terminal event affects persisted evaluation')
            try:
                c.execute('INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)',(self.identifiers.new('event'),applicability_id,event_type,at,now,actor_reference,reason,successor))
                if self._test_failure_hook is not None:
                    self._test_failure_hook()
            except Exception as error:
                raise ValueError('Applicability lifecycle transition blocked') from error
        return event_type

    def revoke(self, authority_id, authority_version, actor_reference, reason):
        return self._transition(authority_id, authority_version, 'REVOKED', actor_reference, reason)

    def _transition(self, aid, version, status, actor, reason):
        if not actor or not reason: raise ValueError('Lifecycle actor and reason are required')
        now=datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')
        with self.repository.transaction() as c:
            old=c.execute('SELECT status FROM authority_state WHERE authority_id=? AND authority_version=?',(aid,version)).fetchone()
            if not old: raise ValueError('Unknown authority')
            c.execute('UPDATE authority_state SET status=?,state_changed_at=? WHERE authority_id=? AND authority_version=?',(status,now,aid,version))
            typ='REVOKED' if status=='REVOKED' else status
            c.execute('INSERT INTO authority_event VALUES (?,?,?,?,?,?,?,?,?)',(self.identifiers.new('event'),aid,version,typ,actor,reason,None,None,now))
        return status

    def supersede(self, predecessor_id, predecessor_version, **successor):
        successor.setdefault('authority_version', predecessor_version+1)
        successor.setdefault('actor_reference','system'); successor.setdefault('reason','superseded')
        with self.repository.transaction() as c:
            row=c.execute('SELECT origin_locator,content_hash,context_revision_id,parameter_reference,effective_from,effective_until FROM governed_authority a JOIN authority_scope s USING(authority_id,authority_version) JOIN authority_temporal_boundary b USING(authority_id,authority_version) WHERE a.authority_id=? AND a.authority_version=?',(predecessor_id,predecessor_version)).fetchone()
            if not row: raise ValueError('Unknown predecessor')
            until=_instant(successor['effective_from'])
            c.execute('UPDATE authority_state SET status=?,state_changed_at=? WHERE authority_id=? AND authority_version=?',('SUPERSEDED',until,predecessor_id,predecessor_version))
            c.execute('INSERT INTO authority_event VALUES (?,?,?,?,?,?,?,?,?)',(self.identifiers.new('event'),predecessor_id,predecessor_version,'SUPERSEDED',successor['actor_reference'],successor['reason'],successor.get('authority_id'),successor['authority_version'],until))
        return self.create_authority(row[0],row[1],row[2],row[3],successor['effective_from'],row[5],successor.get('authority_id'),successor['authority_version'],successor['actor_reference'],successor['reason'])
