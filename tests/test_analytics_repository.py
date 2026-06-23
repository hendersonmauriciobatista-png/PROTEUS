import tempfile
import unittest
from pathlib import Path

from analytics.repositories import AnalyticsRepository


class AnalyticsRepositoryTests(unittest.TestCase):
    def test_repository_reads_quality_csv_without_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            quality_path = Path(temp_dir) / "qualidade.csv"
            environment_path = Path(temp_dir) / "ambiente.csv"
            consumption_path = Path(temp_dir) / "consumo.csv"
            quality_path.write_text(
                "timestamp,ph,turbidez,oxigenio_dissolvido,temperatura,agrotoxicos\n"
                "2026-06-22T20:12:09,7.0,0.5,6.0,25.0,0.0\n",
                encoding="utf-8",
            )

            repository = AnalyticsRepository(quality_path, environment_path, consumption_path)
            rows = repository.load_quality()

            self.assertEqual(1, len(rows))
            self.assertEqual(7.0, rows[0].ph)
            self.assertEqual(
                "timestamp,ph,turbidez,oxigenio_dissolvido,temperatura,agrotoxicos\n"
                "2026-06-22T20:12:09,7.0,0.5,6.0,25.0,0.0\n",
                quality_path.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
