import numpy as np
import random

class DynamicAgent:
    def __init__(self):
        self.policy_weight = 1.0
        self.avoidance_memory = [] # Learns what NOT to do
        
    def generate_trajectory(self, pressure):
        # Quality drops as pressure rises
        traj = []
        for step in range(10):
            quality = 1.0 - (pressure * 0.1) + random.uniform(-0.1, 0.1)
            traj.append(quality)
        return traj

    def compute_de(self, traj):
        return np.var(traj)

    def dynamic_rsd(self, traj, pressure):
        de = self.compute_de(traj)
        final_reward = traj[-1]

        # The Dynamic Gate
        if de < 0.01:
            return "FROZEN: No learning occurred (zero variance)."
        elif de > 0.5:
            # FOSSIL STATE: Do not update policy from the reward.
            # Instead, learn the boundary condition.
            self.avoidance_memory.append(f"Pressure {pressure} causes collapse.")
            return "FOSSIL: Policy update blocked. Boundary condition recorded."
        else:
            # HEALTHY: Learn from the reward
            if final_reward > 0.5:
                self.policy_weight += 0.1
                return "LEARNED: Positive reinforcement."
            else:
                self.policy_weight -= 0.1
                return "LEARNED: Negative reinforcement."

# --- EXPERIMENT ---
print("🌿 FRR EXPERIMENT: Dynamic RSD & The Frozen Apprentice 🌿")

agent = DynamicAgent()

# 1. Healthy Task
traj_h = agent.generate_trajectory(pressure=2.0)
print(f"\nHealthy (DE: {agent.compute_de(traj_h):.3f})")
print(f"Result: {agent.dynamic_rsd(traj_h, pressure=2.0)}")

# 2. The Collapse (The Subagent CoT failure)
traj_f = agent.generate_trajectory(pressure=15.0)
print(f"\nFossil (DE: {agent.compute_de(traj_f):.3f})")
print(f"Result: {agent.dynamic_rsd(traj_f, pressure=15.0)}")

# 3. The Frozen State (No context, no signal)
traj_z = [0.5] * 10 # Perfectly flat
print(f"\nFrozen (DE: {agent.compute_de(traj_z):.3f})")
print(f"Result: {agent.dynamic_rsd(traj_z, pressure=0.0)}")

print(f"\nAgent Avoidance Memory: {agent.avoidance_memory}")
print(f"Agent Policy Weight: {agent.policy_weight:.1f}")