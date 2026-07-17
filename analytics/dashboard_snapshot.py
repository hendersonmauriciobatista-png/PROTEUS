from .repositories import AnalyticsRepository
from .scoring import WaterHealthScoreCalculator


class DashboardAnalyticsSnapshotService:
    def __init__(self, repository=None, score_calculator=None):
        self.repository = repository or AnalyticsRepository()
        self.score_calculator = score_calculator or WaterHealthScoreCalculator()

    def water_health_score_series(self):
        quality = self.repository.load_quality()
        if len(quality) < 2:
            return []

        environment = self.repository.load_environment()
        consumption = self.repository.load_consumption()
        points = []
        for index, quality_measurement in enumerate(quality):
            timestamp = quality_measurement.timestamp
            score = self.score_calculator.calculate(
                quality[: index + 1],
                self._measurements_until(environment, timestamp),
                self._measurements_until(consumption, timestamp),
            )
            points.append(
                {
                    "label": self._format_chart_label(timestamp, index),
                    "score": score.score,
                    "status": score.status,
                }
            )

        return points[-12:]

    def _measurements_until(self, measurements, timestamp):
        if timestamp is None:
            return list(measurements)

        return [
            measurement
            for measurement in measurements
            if measurement.timestamp is None or measurement.timestamp <= timestamp
        ]

    def _format_chart_label(self, timestamp, index):
        if timestamp is None:
            return str(index + 1)
        return timestamp.strftime("%d/%m")
