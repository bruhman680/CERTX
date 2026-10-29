import numpy as np
import random

# Simulate a cognitive state
class Agent:
    def __init__(self):
        self.policy_weight = 1.0  # Starts with a healthy baseline
        
    def generate_trajectory(self, context_pressure):
        # Generate a trajectory of 10 steps. 
        # Step = base_quality - pressure + noise
        trajectory = []
        for step in range(10):
            # Under high pressure, coherence drops rapidly
            quality = 1.0 - (context_pressure * 0.1) + random.uniform(-0.1, 0.1)
            trajectory.append(quality)
        return trajectory

    def compute_dirichlet_energy(self, trajectory):
        # DE measures smoothness. A collapse has erratic high DE, or frozen low DE.
        # Here, we just use variance as a proxy.
        return np.var(trajectory)

    def apply_rsd(self, trajectory, gated=True):
        # The gate checks for fossil state
        de = self.compute_dirichlet_energy(trajectory)
        
        # Healthy DE is between 0.05 and 0.3 (smooth but not frozen)
        is_fossil = de < 0.01 or de > 0.5
        
        if gated and is_fossil:
            return "BLOCKED: Fossil state detected"
            
        # Ungated: Learn from whatever the final state is, even if it was a collapse
        final_reward = trajectory[-1] 
        if final_reward > 0.5:
            self.policy_weight += 0.1
            return "LEARNED: Positive reinforcement"
        else:
            self.policy_weight -= 0.1
            return "LEARNED: Negative reinforcement"

# --- THE EXPERIMENT ---

print("🌿 FRR EXPERIMENT: Gated vs Ungated RSD 🌿")

# 1. Test a healthy trajectory (Low pressure)
agent_a = Agent()
healthy_traj = agent_a.generate_trajectory(context_pressure=1.0)
print(f"\nHealthy Trajectory (DE: {agent_a.compute_dirichlet_energy(healthy_traj):.3f})")
print(f"Ungated RSD: {agent_a.apply_rsd(healthy_traj, gated=False)}")
print(f"Gated RSD:   {agent_a.apply_rsd(healthy_traj, gated=True)}")

# 2. Test a fossil/collapsed trajectory (High pressure - the "Subagent CoT" failure)
agent_b = Agent()
fossil_traj = agent_b.generate_trajectory(context_pressure=15.0) # Massive pressure
print(f"\nFossil Trajectory (DE: {agent_b.compute_dirichlet_energy(fossil_traj):.3f})")
print(f"Ungated RSD: {agent_b.apply_rsd(fossil_traj, gated=False)}")
print(f"Gated RSD:   {agent_b.apply_rsd(fossil_traj, gated=True)}")