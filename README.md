# ASM1 Influent Generator

A Python Module to generate influent data in the Activated Sludge Model 1 (ASM1) format.
This module creates arrays in the format required by the ASM1 model, which is used to simulate the biological processes in wastewater treatment plants. The resulting arrays are resolving to 15 minute time steps and can be used as influent data for the simulation of wastewater treatment plants.


## Getting started

### Installation
Simply install the package with pip:

```bash
pip install asm1-influent-generator
```

### Usage
#### Command Line
There are different ways to use the module. The easiest way is to just call it from the command line:

```bash
asm1-influent-generator 1
```
This will generate one array with 50 days of influent data. The resulting array will be saved as a CSV file in the current working directory.

#### Python
You can also use the module in your own Python code:

```python
from asm1_influent_generator import ASM1Generator

gen = ASM1Generator()
arr = gen.generate(5)
```

This example will generate one array with 5 samples of 50 days of influent data.
The resulting `numpy` array has the shape `(n_samples, n_timesteps, n_components)`.

### Limitations
The module is currently limited to a 50 day generation period. Also, the time step is fixed to 15 minutes.
This is due to the fact, that the underlying Generative Adversarial Network (GAN) was trained on 50 days of 15 minute time steps.


## The Model

We use [`gretel-synthetics`] to generate synthetic data. The model is a [DoppelGANger] model. It was trained on data from the [IWA Benchmark Simulation Model No. 2 (BSM2) influent dataset](https://iwaponline.com/ebooks/book-pdf/650794/wio9781780401171.pdf) which originally features 609 days of influent data. It was trained for 230.000 epochs.

## Credits
The development of this package was done in the context of the [KLÄFFIZIENT] and [KLÄFFIZIENTER] projects. Both projects are funded by the German Federal Ministry for Economic Affairs and Climate Action ([BMWK]) and are part of the 7th and 8th Energy Research Program of the Federal Government.



[`gretel-synthetics`]: https://github.com/gretelai/gretel-synthetics
[DoppelGANger]: http://arxiv.org/abs/1909.13403
[KLÄFFIZIENT]: https://www.evt.tf.fau.de/forschung/schwerpunktekarl/ag-energiesysteme/bmwi-projekt-klaeffizient/
[KLÄFFIZIENTER]: https://www.evt.tf.fau.de/forschung/schwerpunktekarl/ag-energiesysteme/bmwk-projekt-klaeffizienter/
[BMWK]: http://bmwk.de/
