# Flanker task template

This project is to help others get an initial format for psychopy scripts.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

This script is used to run a flanker task in psychopy. It can run either a flanker task using arrows (i.e., <<<<<) or letters (i.e., XXCXX).

### Prerequisites

This project can be run through the coder in the standalone version of psychopy, or though another ide by using the pip install of psychopy and its dependencies.

## Usage

When the script is run you will be prompted to enter a subject number and then you will be asked to enter either an A (for arrow) or L (for letter) to select which type of flanker task you want. Number of valid and invalid trails can be changed by altering the num_valid_trials and num_invalid_trials in the main() function. If you want to keep it on one of types of task (arrow or letter) constantly arrow_vs_letter can be set to either 'a' or 'l' rather than requiring user input.

## License

State the license under which your project is released. For example, you can use a common open-source license like MIT, GNU GPL, or Apache 2.0.

---

Feel free to modify and expand upon this template to fit the specifics of your project. A well-documented README is an essential part of any open-source project, as it helps users and potential contributors understand what your project is about and how to work with it.

