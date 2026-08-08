# Scripts

The **Scripts** directory contains the software used to acquire, process and analyze the measurements presented throughout the **Measurable Science** project.

The primary objective of these scripts is **transparency**, not software engineering.

Every script is intentionally kept as simple as possible so that anyone can inspect its operation, understand what it does, verify the methodology and modify it if necessary.

The goal of this project is **not** to build complex software, but to make scientific measurements accessible to as many people as possible.

---

# Purpose

The scripts included in this repository are used for:

- recording experimental data;
- processing raw datasets;
- extracting carrier signals;
- comparing measurements from different locations;
- investigating signal modulation;
- generating figures and visualizations used throughout the project.

The theoretical background of every analysis is explained in the accompanying book.

---

# Getting Started

All software required to use these scripts is completely **free**.

Before installing Python, it is recommended to install **Visual Studio Code (VS Code)**, which provides a simple environment for editing and running Python scripts.

Recommended software:

- **Visual Studio Code (VS Code)**
- **Python 3**

Both are free and available for Windows, Linux and macOS.

---

# No Programming Experience Required

You do **not** need to be a programmer to participate in this project.

Modern AI assistants can explain every script line by line, help install Visual Studio Code and Python, troubleshoot errors and even modify the scripts for different hardware.

If you have never used Python before, simply ask your preferred AI assistant questions such as:

- How do I install Visual Studio Code?
- How do I install Python?
- How do I run this script?
- Why am I getting this error?
- How do I connect my sensor?
- Can you explain what this script is trying to measure?
- Can you modify this script for my device?

Today's AI tools make it possible for anyone to contribute to scientific research, regardless of programming experience.

---

# Repository Structure

Only a small number of carefully selected scripts are included in this repository.

Each script represents one important part of the research methodology rather than a complete software package.

The repository contains scripts for:

- recording measurements;
- extracting carrier signals;
- comparing recordings from different locations;
- investigating signal modulation;
- visualizing concepts discussed throughout the project.

Each script contains comments explaining its purpose, expected input and generated output.

---

# Script Philosophy

These scripts are intended to demonstrate the research methodology rather than provide a complete software framework.

Only the scripts required to understand and reproduce the methodology are published.

The objective is **not** to require researchers to use these exact scripts.

Instead, the goal is to explain the methodology clearly enough that anyone can:

- reproduce the measurements;
- modify the existing scripts;
- adapt them to different hardware;
- develop completely new implementations.

Independent implementations are encouraged.

Scientific progress comes from reproducible methods rather than identical software.

---

# Open Source Philosophy

These scripts are provided as transparent research tools.

Everyone is encouraged to:

- inspect the source code;
- repeat the measurements;
- improve existing methods;
- develop new analytical approaches;
- report problems;
- contribute improvements.

The methodology is open, and every improvement benefits the entire research community.

---

# Methodology

The complete measurement methodology is described in the **Methodology** section of this repository.

Representative experimental recordings are available in the **Locations** directory.

These scripts provide the connection between the published raw data and the analyses presented in the accompanying book.

---

# Open Research

This repository is not intended to provide final answers.

Its purpose is to provide transparent tools that allow anyone to independently investigate the questions discussed throughout the project.

Researchers are encouraged to perform their own measurements, compare results, improve the methodology and publish independent analyses.

# Project Workflow

The recommended order of the scripts is:

**01 Recording**

↓

**02 Normalization**

↓

**03 Carrier Discovery**

↓

**04 Carrier Characterization**

↓

**05 Further Analysis**

Following this order keeps the analysis simple and avoids searching the entire frequency spectrum manually.