"""Nodo eNB. Relay radio (RRC) <-> NAS/S1 (MME). Correr:  python enb.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "eNB"


def _ue_de_session(session):
    return "UE1" if (session or "").startswith("ue1") else "UE2"


class ENB(Node):
    def handle(self, env):
        a = env["action"]
        src = env["Node_origin"]
        payload = env.get("payload", {})
        if a == "RRC_CONNECTION_REQUEST":
            return [("RRC_CONNECTION_SETUP", src, {})]
        if a == "RRC_CONNECTION_SETUP_COMPLETE":
            return [("ATTACH_REQUEST", "MME", payload)]
        if a == "E_RAB_SETUP_REQUEST":
            # Viene del MME -> reconfigurar la radio del UE correspondiente
            ue = _ue_de_session(env.get("session"))
            return [("RRC_CONNECTION_RECONFIGURATION", ue, payload)]
        if a == "RRC_CONNECTION_RECONFIGURATION_COMPLETE":
            return [("E_RAB_SETUP_RESPONSE", "MME", {})]
        if a == "UPLINK_DIRECT_TRANSFER":
            return [("ATTACH_COMPLETE", "MME", payload)]
        return []


if __name__ == "__main__":
    ENB(NODE).run()
