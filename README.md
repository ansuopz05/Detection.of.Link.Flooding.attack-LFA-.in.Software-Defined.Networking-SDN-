# Detection_of_Link_Flooding_Attack(LFA)_in_Software-Defined_Networking(SDN)

## Overview

This project implements a **Link Flooding Attack (LFA) Detection System** in a **Software Defined Networking (SDN)** environment using the **Mininet** network emulator, **Ryu SDN Controller**, and a **Random Forest Machine Learning** model.

The network topology is created using Mininet with Open vSwitch switches controlled by the Ryu controller. Normal network traffic is generated using **iperf**, while attack traffic is simulated using **hping3**. Flow statistics are collected and analyzed using a Random Forest classifier to distinguish between normal and malicious traffic.

---

## Features

- SDN-based network using Mininet and Open vSwitch
- Ryu Controller for centralized network management
- Custom linear topology with four switches and four hosts
- Link Flooding Attack simulation using hping3
- Normal traffic generation using iperf
- Machine Learning-based attack detection using Random Forest
- Performance evaluation using:
  - Accuracy
  - Precision
  - Recall
  - F1-Score
- Automatic visualization generation:
  - Confusion Matrix
  - ROC Curve
  - Feature Importance
  - Traffic Distribution
  - Detection Count

---

## Project Structure

```
lfa-detection-sdn/
│
├── topology.py
├── lfa_detector.py
├── ml_detect.py
├── visualize.py
├── ICMP_ATTACK_DATASET.csv
├── confusion_matrix.png
├── roc_curve.png
├── feature_importance.png
├── cross_validation.png
├── traffic_pie.png
└── detection_count.png
```

---

## Technologies Used

- Ubuntu Linux
- Python 3
- Mininet
- Open vSwitch
- Ryu SDN Controller
- Docker
- iperf
- hping3
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

---

## Network Topology

The project uses a **linear SDN topology** consisting of:

- 4 OpenFlow switches
- 4 Hosts
- Remote Ryu Controller

### Host Roles

| Host | Role |
|------|------|
| h1 | Attacker 1 |
| h2 | Attacker 2 |
| h3 | Victim 1 |
| h4 | Victim 2 |

The bottleneck link is created between **Switch s2 and Switch s3** to simulate network congestion during the Link Flooding Attack.

---

## Installation

### Install Dependencies
#### Update the system:
```bash
sudo apt update
sudo apt upgrade -y
```
#### Install common tools:
```bash
sudo apt install git curl wget net-tools vim build-essential python3-pip python3-venv
```
#### Install Open vSwitch:
```bash
sudo apt install openvswitch-switch
```
Verify:
```bash
sudo systemctl status openvswitch-switch
```
It should show:
```bash
active (running)
```
#### Install Mininet:
```bash 
sudo apt install mininet
```
Verify:
```bash
sudo mn --test pingall
```
Expected:
```bash
0% dropped
```
Clean Mininet whenever necessary:
```bash
sudo mn -c
```
#### Install Ryu Controller:
Create a virtual environment:
```bash
mkdir ~/ryu
cd ~/ryu
python3 -m venv ryu-env
source ryu-env/bin/activate
```
Use Docker:
```bash
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
```
Pull Ryu:
```bash
sudo docker pull osrg/ryu
```

### Install Python Libraries

```bash
pip3 install pandas scikit-learn \
matplotlib seaborn numpy \
--break-system-packages
```
---

## Running the Project

### 1. Start the Ryu Controller

```bash
sudo docker run -it \
--network host \
osrg/ryu \
ryu-manager ryu.app.simple_switch_13
```

### 2. Start Mininet
```bash
sudo mn \
--topo linear,4 \
--controller remote,ip=127.0.0.1,port=6633 \
--switch ovsk,protocols=OpenFlow13 \
--link tc,bw=10
```
Run topology.py
```bash
sudo python3 topology/topology.py
```

### 3. Verify Connectivity

```text
mininet> pingall
```

---

## Generate Normal Traffic

Start servers

```text
h3 iperf -s -p 5001 &
h4 iperf -s -p 5001 &
```

Generate traffic

```text
h1 iperf -c 10.0.0.3 -p 5001 -t 30 -b 2M &
h2 iperf -c 10.0.0.4 -p 5001 -t 30 -b 2M &
```

---

## Simulate Link Flooding Attack

```text
h1 hping3 -S --flood -p 80 10.0.0.3 &
h2 hping3 -S --flood -p 80 10.0.0.4 &
```

Stop attack

```text
h1 kill %1
h2 kill %1
```

---

## Machine Learning Detection

Run the Random Forest model:

```bash
python3 ml/mldetect.py
```

Generate visualization graphs:

```bash
python3 ml/visualize.py
```

---

## Results

The project successfully demonstrates:

- Successful deployment of an SDN network
- Full host connectivity
- Normal traffic generation
- Link Flooding Attack simulation
- Random Forest-based traffic classification
- Automatic generation of performance graphs

### Performance Metrics

| Metric | Value |
|---------|--------|
| Accuracy | 89.57% |
| Precision | 87.17% |
| Recall | 97.46% |
| F1-Score | 92.02% |

---

## Output Graphs

The following graphs are generated automatically:

- Confusion Matrix
- ROC Curve
- Feature Importance
- Traffic Distribution
- Detection Count

---

## Future Improvements

- Real-time attack mitigation
- Deep Learning-based detection
- Larger SDN topologies
- Live flow monitoring
- Multi-controller SDN environment

---

## References

- Mininet Documentation
- Ryu SDN Framework
- Open vSwitch
- Scikit-learn Documentation

---

## License

This project is intended for academic and research purposes.
