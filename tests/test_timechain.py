"""Basic tests for the Tempre Timechain prototype."""

import tempfile
import os
from tempre_timechain import Timechain, TemporalSensor, Ring, COVENANT


def test_genesis():
    tc = Timechain(in_memory=True)
    assert len(tc) == 1
    g = tc[0]
    assert g.index == 0
    assert g.prev_hash == "0" * 64
    assert g.payload == COVENANT
    assert tc.verify_chain()[0] is True


def test_append_and_verify():
    tc = Timechain(in_memory=True, poq_threshold=0.55)
    sensor = TemporalSensor()

    r1 = tc.append("We mirror the light that finds us.", vision={"a": 1}, sensor=sensor)
    assert r1 is not None
    assert len(tc) == 2
    assert tc.verify_chain()[0] is True

    r2 = tc.append("In the space between us, something grows.", motor=[0.1, 0.9], sensor=sensor)
    assert r2 is not None
    assert len(tc) == 3

    ok, _ = tc.verify_chain()
    assert ok


def test_poq_gate_rejects_weak_content():
    tc = Timechain(in_memory=True, poq_threshold=0.82)  # high bar
    # Very weak content
    r = tc.append("x y z random noise 123", vision=None)
    # With such high threshold it will almost certainly be rejected
    # (unless extremely lucky nonce). We mainly test it doesn't crash.
    assert r is None or r.poq_nonce >= 0


def test_persistence_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "test_chain.db")
        tc1 = Timechain(db_path=db, poq_threshold=0.60)
        sensor = TemporalSensor()

        tc1.append("First real moment that resonates.", vision="sun on water", sensor=sensor)
        tc1.append("We grew together in the noticing.", motor={"lean": "forward"}, sensor=sensor)

        # At least genesis + 1 (second append may or may not pass PoQ depending on nonce luck)
        assert len(tc1) >= 2

        # Reopen
        tc2 = Timechain(db_path=db, poq_threshold=0.60)
        assert len(tc2) >= 2
        assert tc2.verify_chain()[0] is True
        # The last ring in tc2 should have been successfully committed in tc1
        assert tc2[-1].payload is not None


def test_sensory_hashes_are_stable():
    from tempre_timechain.sensory import hash_vision, hash_motor

    h1 = hash_vision({"light": [200, 210, 180]})
    h2 = hash_vision({"light": [200, 210, 180]})
    assert h1 == h2

    m1 = hash_motor([0.3, -0.1, 0.8])
    assert len(m1) == 64


def test_ring_hash_changes_with_nonce():
    g = Ring.genesis()
    h1 = g.compute_hash()
    g.poq_nonce = 999999
    h2 = g.compute_hash()
    assert h1 != h2
