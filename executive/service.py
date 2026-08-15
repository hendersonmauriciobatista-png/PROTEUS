from datetime import datetime

from analytics import AnalyticsService
from executive_recommendation import ExecutiveRecommendationService
from governance import OperationalGovernanceService

from .models import ExecutiveSnapshot
from .rules import ExecutiveRules


class ExecutiveIntelligenceService:
    def __init__(self, analytics_service=None, governance_service=None, rules=None, recommendation_service=None):
        self.analytics_service = analytics_service or AnalyticsService()
        self.governance_service = governance_service or OperationalGovernanceService()
        self.rules = rules or ExecutiveRules()
        self.recommendation_service = recommendation_service or ExecutiveRecommendationService()

    def build_snapshot(self):
        analytics_snapshot = self.rules.filter_analytics_snapshot(self.analytics_service.build_snapshot())
        events = self.rules.filter_events(self.governance_service.list_events())
        persisted_summary = self.governance_service.summarize_by_state()
        summary = {
            state: sum(1 for event in events if event.state == state)
            for state in persisted_summary
        }

        executive_status, explanations = self.rules.classify_status(analytics_snapshot, events)
        relevant_alerts = self.rules.select_relevant_alerts(analytics_snapshot.alerts)
        key_trends = self.rules.select_key_trends(analytics_snapshot)
        priorities = self.rules.build_priorities(
            analytics_snapshot,
            events,
            relevant_alerts,
            key_trends,
        )
        recommendation_snapshot = self.recommendation_service.build_snapshot(
            analytics_snapshot=analytics_snapshot,
            governance_snapshot=summary,
            observational_result=None,
        )

        return ExecutiveSnapshot(
            generated_at=datetime.now(),
            water_health_score=analytics_snapshot.water_health_score.score,
            water_health_status=analytics_snapshot.water_health_score.status,
            executive_status=executive_status,
            open_events=summary.get("ABERTO", 0),
            monitoring_events=summary.get("MONITORAMENTO", 0),
            resolved_events=summary.get("RESOLVIDO", 0),
            archived_events=summary.get("ARQUIVADO", 0),
            relevant_alerts=relevant_alerts,
            key_trends=key_trends,
            executive_message=self.rules.executive_message(executive_status),
            observational_priorities=priorities,
            explanations=explanations,
            recommendation_snapshot=recommendation_snapshot,
        )
