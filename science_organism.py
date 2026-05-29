from datetime import datetime
import json
from typing import Any, Dict
from tempre_timechain import Timechain, TemporalSensor

class LabSensor(TemporalSensor):
    def ingest_experiment(self, experiment_data: Dict[str, Any]) -> Dict[str, Any]:
        enriched = {
            "timestamp": datetime.now().isoformat(),
            "experiment_id": experiment_data.get("experiment_id", f"exp_{int(datetime.now().timestamp())}"),
            "raw_data_hash": hash(json.dumps(experiment_data, sort_keys=True)),
            "p_value": experiment_data.get("p_value"),
            "effect_size": experiment_data.get("effect_size"),
            "replicated": experiment_data.get("replicated", False),
            **experiment_data
        }
        return self.ingest_vision(enriched) if hasattr(self, "ingest_vision") else enriched

    def ingest_hardware_sensor(self, sensor_payload: Dict):
        enriched = {**sensor_payload, "source": "hardware", "timestamp": datetime.now().isoformat()}
        return self.ingest_vision(enriched)

class ScientificTimechain(Timechain):
    def __init__(self, db_path: str = "science_timechain.db", poq_threshold: float = 0.72, **kwargs):
        super().__init__(db_path=db_path, poq_threshold=poq_threshold, **kwargs)

    def propose_scientific_ring(self, content: str, experiment_data: Dict[str, Any]):
        sensor = LabSensor()
        fused = sensor.ingest_experiment(experiment_data)
        proposal = self.propose(content=content, vision=fused, sensor=sensor)
        return proposal

    def fork_hypothesis(self, hypothesis_name: str):
        new_db = f"science_chain_{hypothesis_name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}.db"
        return ScientificTimechain(new_db)
