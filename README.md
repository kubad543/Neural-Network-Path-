# Autonomous Vehicle Navigation with NEAT and Pygame

## Screenshots
- **Vehicle Visualization:** ![Vehicle Visualization](path_to_image)
- **Map Visualization:** ![Map Visualization](path_to_image)
- **Original Map (before 2D transformation):** ![Original Map](path_to_image)
- **Generated Trajectory:** ![Generated Trajectory](path_to_image)

---

## Project Overview

This project simulates an autonomous vehicle navigating through different environments using **NEAT (NeuroEvolution of Augmenting Topologies)** and **Pygame** for visualization. The vehicle learns how to reach the target while avoiding obstacles through an evolutionary process, improving its performance over successive generations. The neural network, which controls the vehicle, is trained based on a **fitness function** that evaluates the efficiency of the generated trajectory. Rewards are given for reaching the target, staying oriented towards it, and avoiding obstacles, while penalties are applied for collisions or getting too close to obstacles. The learning process is adjusted dynamically based on fitness evaluation, ensuring the vehicle becomes more efficient over time.

### 🚗 **Key Features**
The vehicle autonomously finds optimal paths to a target on various maps while detecting obstacles using radar sensors. It is controlled by a neural network that receives sensor data and outputs steering decisions. The simulation uses **Pygame** to render the vehicle, maps, and real-time trajectories. The fitness function rewards the vehicle for minimizing distance to the target, avoiding collisions, and maintaining efficient movement patterns. Collisions and being too close to obstacles result in penalties. Performance tracking logs the best distances and success rates for each map and generation.

### ⚙️ **Technologies Used**
- **Python:** The main programming language that drives the simulation logic and evolutionary algorithm.
- **Pygame:** A library used to handle graphics and render the vehicle, maps, and trajectories in real-time.
- **NEAT (Python-neat library):** An evolutionary algorithm used to optimize the neural network's decision-making process. It evolves the neural network over generations, selecting the best agents and introducing mutations to create new candidates for future learning.
- **config.txt file:** This configuration file allows setting the initial parameters for the simulation, such as the number of individuals per epoch, mutation rates, and other NEAT parameters. For example, the `population_size` setting in `config.txt` defines how many agents are present per generation.

### 🧠 **How It Works**
The neural network controlling the vehicle is designed to process inputs from various sensors mounted on the robot. These sensors measure distances to obstacles and provide information on the robot's current position, speed, and rotation. The network processes this data to generate control signals (outputs) that steer the vehicle and adjust its speed and direction. These outputs include steering angle changes, acceleration, or deceleration commands. 

The vehicle's behavior is shaped by a reward-and-penalty mechanism where rewards are given for moving toward the target, reaching it, and avoiding obstacles. Penalties are applied for collisions or getting too close to obstacles, forcing the network to adjust its decision-making. 

The evolutionary process is governed by NEAT, which evolves the neural network over multiple generations, selecting the best-performing agents (vehicles) based on their fitness scores and introducing random mutations. Over time, this allows the vehicle to improve its navigation ability, making it more efficient at reaching the target while avoiding obstacles.

### 🧠 **Neural Network Inputs and Outputs**
- **Inputs:** The neural network receives data from sensors mounted on the vehicle, which includes information on the distance to obstacles and the robot's current state (speed, rotation angle, position). These inputs allow the network to assess its environment and make informed decisions about its movement.
  
- **Outputs:** The neural network generates control commands based on the sensor data. These outputs dictate the robot's movements, such as changes in the steering angle, adjustments in speed, and decisions on the direction to move (e.g., left, right, forward, speed).
