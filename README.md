# Autonomous Vehicle Navigation with NEAT and Pygame

## Screenshots
- **Vehicle Visualization:** *(Insert screenshot of the vehicle here)*
- **Map Visualization:** *(Insert screenshot of the map here)*
- **Original Map (before 2D transformation):** *(Insert screenshot of the original map here)*
- **Generated Trajectory:** *(Insert screenshot of the vehicle's path here)*

---

## Project Overview

This project simulates an autonomous vehicle navigating through different environments using **NEAT (NeuroEvolution of Augmenting Topologies)** and **Pygame** for visualization. The vehicle learns how to reach the target while avoiding obstacles through an evolutionary process, improving its performance over successive generations.

### 🚗 **Key Features**
- **Autonomous Navigation:** The vehicle autonomously finds optimal paths to a target on various maps.
- **Collision Detection:** Accurate obstacle detection using radar sensors and pixel-based collision checks.
- **Dynamic Learning:** Real-time adjustment of strategies based on fitness evaluation, including penalties for inefficient behaviors like spinning or collisions.
- **Performance Tracking:** Logs the best distances and success rates for different maps, providing insights into learning progress.

### ⚙️ **Technologies Used**
- **Python:** Core programming language for the simulation logic.
- **Pygame:** Handles graphics, rendering the vehicle, maps, and real-time trajectories.
- **NEAT (Python-neat library):** Implements neuroevolution for optimizing the vehicle’s decision-making process.

### 🧠 **How It Works**
1. **Neural Network Control:** Each vehicle is controlled by a neural network, which receives radar data (distances to obstacles) as inputs and outputs steering decisions.
2. **Sensor System (Radar):** Virtual radars detect obstacles within a 300-pixel range in multiple directions, providing spatial awareness.
3. **Fitness Function:** Rewards the vehicle for minimizing distance to the target, avoiding collisions, and maintaining efficient movement patterns.
4. **Evolutionary Algorithm:** NEAT evolves the neural networks over generations, selecting the best-performing agents and mutating them to create new candidates.

### 📊 **Statistics & Analysis**
- Tracks generation-wise performance improvements.
- Records the best trajectories for each map.
- Logs success rates, including metrics like:
  - **Appearances:** How many times a map was used.
  - **Successes:** How often the vehicle reached the target.

---

*This project demonstrates the power of combining neuroevolution with real-time simulations for autonomous vehicle navigation.*
