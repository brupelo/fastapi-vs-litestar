# Python Web Framework Benchmark: fastapi vs litestar

This repository contains benchmarking scripts and configurations for comparing
two prominent Python web frameworks: [fastapi](https://pypi.org/project/fastapi/) and [litestar](https://pypi.org/project/litestar/). The goal is to
provide an objective comparison focusing on performance, ease of use, and
adherence to best practices. The benchmarks aim to ensure fairness and accuracy
in evaluating these frameworks for various use cases and workloads.

## Purpose

The purpose of this project is to conduct a comprehensive and fair comparison
between fastapi and litestar, two modern Python web frameworks. Through a
series of tests and stress tests, we aim to evaluate their performance,
robustness, and adherence to best practices in web development. The intention
is to assist developers in making informed decisions when selecting a framework
for their projects.

## Requirements

- [Just](https://github.com/casey/just) - Command runner tool

## Usage

To start benchmarking and comparing the two frameworks, follow these steps:

1. Create a virtual environment and activate it using your preferred method.
2. Install the package by running the command:
    ```bash
    pip install -e .
    ```

## Basic Tests

Run basic tests to evaluate the basic functionalities of the frameworks:

- fastapi:
    ```bash
    just test-fastapi
    ```

- litestar:
    ```bash
    just test-litestar
    ```

## Stress Tests

Conduct stress tests to analyze the performance and stability under heavy load:

- fastapi:
    ```bash
    just stress-fastapi
    ```

- litestar:
    ```bash
    just stress-litestar
    ```

## Available Tasks

For a list of available tasks, run:
```bash
just -l
```
