from kernel.decision_core.mu02_decision_core import MU02DecisionCore

# 模擬 MC01（簡化版）
class MockMC:
    def export_state(self):
        return {
            "pain": 0.4,
            "tolerance": 0.2,
            "l1_size": 10,
            "l2_size": 20
        }

mc = MockMC()
mu02 = MU02DecisionCore(mc)

# 測試輸入
packet = {
    "content": "這是一個測試任務，請立即執行",
    "delta_s": 0.6
}

for i in range(10):
    result = mu02.evaluate_task(packet)
    print(i, result)
