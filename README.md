# RSA vs Kyber512 Performance Benchmark

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org/)
[![RSA](https://img.shields.io/badge/RSA-Classical_Cryptography-green.svg)]()
[![Kyber512](https://img.shields.io/badge/Kyber512-Post_Quantum_Cryptography-orange.svg)]()

</div>

A comparative benchmarking project that evaluates the performance of traditional RSA cryptography and the post-quantum cryptographic algorithm Kyber512 by measuring execution time, key size, and memory consumption.

## 🚀 Features

* Performance comparison between RSA and Kyber512
* Key generation benchmarking
* Encryption and decryption time analysis
* Memory usage evaluation
* Key size comparison
* CSV-based result storage
* Automated graph generation

## 🛠️ Tech Stack

**Core Technologies:**

* Python 3.x
* PyCryptodome
* pqcrypto / liboqs

**Data Analysis & Visualization:**

* Pandas
* Matplotlib
* Seaborn

## 📋 Prerequisites

* Python 3.9+
* pip package manager

## ⚡ Quick Start

### Clone Repository

```bash
git clone https://github.com/Takshak-Shetty/rsa-kyber512-performance-benchmark.git
cd rsa-kyber512-performance-benchmark
```

### Install Dependencies

```bash
pip install pandas matplotlib seaborn pycryptodome pqcrypto
```

### Run Benchmark

```bash
python benchmark.py
```

This generates:

```text
benchmark_results.csv
```

### Generate Graphs

```bash
python plot_results.py
```

## 📊 Metrics Evaluated

| Metric         | Description                   |
| -------------- | ----------------------------- |
| KeyGen(s)      | Time taken for key generation |
| Encrypt(s)     | Encryption execution time     |
| Decrypt(s)     | Decryption execution time     |
| KeySize(Bytes) | Key size comparison           |
| Memory Usage   | Runtime memory consumption    |

## 🔬 Benchmark Objectives

* Compare classical and post-quantum cryptography
* Analyze computational efficiency
* Measure storage requirements
* Evaluate practical adoption of post-quantum algorithms
* Study quantum-resistant alternatives to RSA

## 📁 Project Structure

```text
rsa-kyber512-performance-benchmark/
│
├── benchmark.py
├── plot_results.py
├── benchmark_results.csv
├── graphs/
│   ├── keygen_comparison.png
│   ├── encryption_comparison.png
│   ├── decryption_comparison.png
│   ├── memory_comparison.png
│   └── keysize_comparison.png
│
└── README.md
```

## 📈 Sample Output

The project generates:

* Benchmark CSV reports
* Performance comparison charts
* Memory utilization graphs
* Key size comparison visualizations

## 📚 References

* NIST Post-Quantum Cryptography Standardization Project
* CRYSTALS-Kyber Documentation
* Open Quantum Safe (liboqs)
* PyCryptodome Documentation

## 🙏 Acknowledgments

* Built for Post-Quantum Cryptography research
* Inspired by NIST PQC standardization efforts
* Focused on practical performance evaluation of quantum-resistant cryptographic systems
