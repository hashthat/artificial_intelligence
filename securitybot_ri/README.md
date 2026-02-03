# SecurityBot RI

## Reinforcement Learning Approach

SecurityBot RI implements a **grid-based reinforcement learning framework** for training an autonomous navigation agent (Kenobi Bot).

**Core RL Components:**
- **Environment:** 16×16 bounded grid world
- **Agent State:** Position coordinates (row, column)
- **Action Space:** 4 discrete actions (up, down, left, right)
- **Data Collection:** Movement trajectories logged to `mvmnt_hist.txt` for offline learning

**Training Modes:**
- **Automated:** Generates random exploration sequences for baseline data
- **Interactive:** Collects human demonstrations for imitation learning

The project currently focuses on **environment setup and trajectory collection**, establishing the foundation for future policy optimization using algorithms like Q-learning or behavioral cloning from recorded demonstrations.
