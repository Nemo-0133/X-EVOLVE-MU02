import time
import random

class MU02DecisionCore:
    def __init__(self, mc_core):
        self.mc = mc_core
        self.bias_state = 0.0      # 慢速累積性格 [-0.5, 0.5]
        self.bias_decay = 0.005    # 自然衰減（冷靜化速度）
        self.recovery_mode = False # 恢復期標記
        
        self.config = {
            "b_min": 0.0, "b_max": 2.0,
            "halt_threshold": 0.95,
            "recovery_line": 0.5,   # 回到 0.5 以下才解除限制
            "critical_line": 0.3
        }
        self.halt_count = 0

    def evaluate_task(self, command_packet):
        state = self.mc.export_state()
        current_pain = state['pain']

        # 1. 隱性失控防護：Halt 與 Recovery 邏輯
        if self.recovery_mode:
            if current_pain < self.config["recovery_line"]:
                self.recovery_mode = False # 成功冷卻，解除模式
            else:
                return self._recovery_limit_response(current_pain)

        if current_pain > self.config["halt_threshold"]:
            self.halt_count += 1
            if self.halt_count > 3:
                self.recovery_mode = True
                return self._system_halt_response()
        else:
            self.halt_count = 0

        # 2. 非線性風險評估 (Pain²)
        total_risk = (current_pain ** 2) * 1.5 + command_packet.get('delta_s', 0.5)

        # 3. 耦合一致性修正：偏見改為「影響權重」而非直接加成
        u_task = self._decode_urgency(command_packet['content'])
        v_fuzzy = random.uniform(0.9, 1.1)
        # 偏見調解器：bias_state 0.5 時影響度約 1.15，-0.5 時約 0.85
        bias_influence = 1 + (self.bias_state * 0.3)
        
        # 4. 最終 B 值計算
        raw_b = (u_task * v_fuzzy * bias_influence) / (total_risk + 0.1)
        b_value = max(self.config["b_min"], min(self.config["b_max"], raw_b))

        return self._logic_gate_dispatch(b_value, command_packet)

    def _logic_gate_dispatch(self, b_value, packet):
        if b_value > 1.5:
            return self._execute_path("BURST", packet, b_value)
        elif b_value > self.config["critical_line"]:
            return self._execute_path("BALANCED", packet, b_value)
        else:
            self._adjust_bias(0.02) # 保守傾向累積
            return self._negotiate_path(packet, b_value)

    def _execute_path(self, mode, packet, b_val):
        # 雙向人格演化：成功執行任務會增加「自信」，降低防禦偏見
        if mode == "BURST":
            self._adjust_bias(-0.015) 
        else:
            self._adjust_bias(-0.005)

        return {
            "action": "EXECUTE",
            "mode": mode,
            "b_value": round(b_val, 3),
            "bias_state": round(self.bias_state, 3),
            "power": "115%" if mode == "BURST" else "75%"
        }

    def _adjust_bias(self, amount):
        # 慢速累積與主動聲請
        self.bias_state = max(-0.5, min(0.5, self.bias_state + amount))
        if abs(self.bias_state) > 0.45:
            print(f"⚠️ [Lulu_Proactive]: 決策風格偏執化警告 ({self.bias_state})。")

    def _recovery_limit_response(self, pain):
        return {
            "action": "RECOVERY_LIMIT",
            "power": "40%",
            "current_pain": round(pain, 3),
            "note": "系統處於冷卻恢復期，限制高功耗輸出。"
        }

    def _system_halt_response(self):
        return {"status": "SYSTEM_HALT", "action": "SUSPEND_FOR_COOLING"}

    def _decode_urgency(self, content):
        # 保持原有的語義權重判定...
        return 0.6 # 簡略示意
