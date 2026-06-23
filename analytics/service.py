from .alerts import PreventiveAlertService
from .models import AnalyticsSnapshot
from .repositories import AnalyticsRepository
from .scoring import WaterHealthScoreCalculator
from .trends import TrendAnalyzer


class AnalyticsService:
    def __init__(self, repository=None, trend_analyzer=None, alert_service=None, score_calculator=None):
        self.repository = repository or AnalyticsRepository()
        self.trend_analyzer = trend_analyzer or TrendAnalyzer()
        self.alert_service = alert_service or PreventiveAlertService()
        self.score_calculator = score_calculator or WaterHealthScoreCalculator()

    def build_snapshot(self):
        quality = self.repository.load_quality()
        environment = self.repository.load_environment()
        consumption = self.repository.load_consumption()

        quality_trends = self.trend_analyzer.quality_trends(quality)
        consumption_trends = self.trend_analyzer.consumption_trends(consumption)
        alerts = self.alert_service.build_alerts(
            quality,
            environment,
            consumption,
            quality_trends,
            consumption_trends,
        )
        score = self.score_calculator.calculate(quality, environment, consumption)

        return AnalyticsSnapshot(
            quality_trends=quality_trends,
            consumption_trends=consumption_trends,
            alerts=alerts,
            water_health_score=score,
        )
