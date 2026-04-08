# X-EVOLVE-MU02

## 🧠 MU-02 Decision Core

MU-02 是 X-EVOLVE 系統的「決策層核心」。

它負責：
- 任務風險評估（Pain-based nonlinear risk）
- 行為決策（BURST / BALANCED / NEGOTIATE）
- 偏見演化（Bias Evolution）
- 系統穩定保護（Halt & Recovery Mode）

---

## ⚙️ Core Logic

B-value formula:

B = (U_task * V_fuzzy * Bias Influence) / (Total Risk + ε)

---

## 🔁 Key Features

- Nonlinear Risk Model (Pain²)
- Bias as Modulator (not override)
- Recovery Mode (post-overload stabilization)
- Adaptive personality evolution

---

## 📂 Structure

kernel/decision_core/mu02_decision_core.py

---

## 🚧 Status

Stable (Audited Version)

---

## 🔜 Next

MU-03 Behavior Monitor
