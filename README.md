# Measurement Software

## Overview

Measurement Software is a Python package for controlling and automating a variety of laboratory measurement instruments. It provides a unified interface for experiment setup, data acquisition, and instrument management, enabling users to streamline workflows and automate repetitive tasks.

## Features

- Modular instrument control via SCPI commands
- Easy integration of new instruments with automation scripts
- Experiment templates for rapid prototyping
- Data auto-saving and management
- Helper utilities for common measurement tasks
- Network manager for multi-instrument setups

## Instruments Supported

- Signal Generator
- Tracking Generator
- Vector Network Analyzer (VNA)
- Oscilloscope (Rigol)
- Spectrum Analyzer (Signal Hound)
- Additional instruments can be added using provided templates

## Getting Started

1. **Clone the repository**  
  `git clone <repo-url>`

2. **Install dependencies**  
  See `requirements.txt` for required Python packages.

3. **Run an experiment**  
  Use the provided experiment templates in the `Experiments/` directory to get started.

4. **Add a new instrument**  
  Follow the instructions in `Instruments/AddANewInstrument.ipynb` to integrate new hardware.

## Folder Structure

- `Instruments/` — Instrument drivers and helpers
- `Experiments/` — Example and template experiments
- `Reference/` — Simulation notebooks and documentation
- `README.md` — Project overview and instructions

## Contributing

Contributions are welcome! Please submit pull requests or open issues for bugs and feature requests.

## TODO

- Add automation script for new instrument creation
- Improve documentation for instrument integration
- Review and clarify overlap vs sequential command handling


