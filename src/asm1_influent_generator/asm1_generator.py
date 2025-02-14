import os
from typing import Optional

import numpy as np
import torch
from gretel_synthetics.timeseries_dgan.dgan import DGAN


class ASM1Generator:
    def __init__(self, model_name: Optional[str] = None, device: str = 'cpu'):
        """
        Initializes the ASM1Generator class.

        Parameters
        ----------
        model_name : str
            Model to be used for the generation of influent data.
        device : str
            Device to be used - most commonly 'cpu' or 'cuda'. Default is 'cpu'.
        """
        if model_name is None:
            model_name = 'bsm2_dgan_model_230400iter.pt'

        # Get the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Join the current directory with the model name
        model_path = os.path.join(current_dir, model_name)

        self.model = DGAN.load(model_path, map_location=torch.device(device))

    @classmethod
    def __moving_average(cls, x, w):
        y = np.zeros((x.shape[0], x.shape[1] - w + 1, x.shape[2]))
        for i in range(x.shape[0]):
            for j in range(x.shape[2]):
                y[i, :, j] = np.convolve(x[i, :, j], np.ones(w), 'valid') / w
        return y

    def generate(self, n_samples: int = 1, components: Optional[list[str]] = None, smoothing: int = 18) -> np.ndarray:
        """
        Generates influent data using the specified model.

        Parameters
        ----------
        n_samples : int
            Number of samples to generate.
        components : list
            List of components to generate. If empty, all components will be generated:
            ("SI", "SS", "XI", "XS", "XBH", "XBA", "XP", "SO", "SNO", "SNH", "SND",
             "XND", "SALK", "TSS", "Q", "TEMP", "SD1", "SD2", "SD3", "XD4", "XD5")

        Returns
        -------
        np.ndarray
            Generated influent data. The shape of the array is (n_samples, n_timesteps, n_components).
        """
        asm1_components = [
            'SI',
            'SS',
            'XI',
            'XS',
            'XBH',
            'XBA',
            'XP',
            'SO',
            'SNO',
            'SNH',
            'SND',
            'XND',
            'SALK',
            'TSS',
            'Q',
            'TEMP',
            'SD1',
            'SD2',
            'SD3',
            'XD4',
            'XD5',
        ]
        if components is not None:
            components = [c.upper() for c in components]
            for c in components:
                if c not in asm1_components:
                    msg = f'Component {c} not found in ASM1 components.'
                    raise ValueError(msg)
        else:
            components = asm1_components
        _, arr = self.model.generate_numpy(n_samples)
        arr = np.array(arr)
        arr = self.__moving_average(arr, smoothing)
        arr_labels = ('SI', 'SS', 'XI', 'XS', 'XBH', 'SNH', 'SND', 'XND', 'SALK', 'TSS', 'Q', 'TEMP')

        const_values = {
            'XBA': 0,
            'XP': 0,
            'SO': 0,
            'SNO': 0,
            'SALK': 7,
            'SD1': 0,
            'SD2': 0,
            'SD3': 0,
            'XD4': 0,
            'XD5': 0,
        }

        out = np.zeros((arr.shape[0], arr.shape[1], len(components)))
        for num in range(arr.shape[0]):
            for idx, component in enumerate(components):
                if component in arr_labels:
                    out[num, :, idx] = arr[num, :, arr_labels.index(component)]
                elif component in const_values:
                    out[num, :, idx] = const_values[component]
                else:
                    msg = f'Component {c} not found in ASM1 components.'
                    raise ValueError(msg)

        # Time index is the first column
        timestep = 15 / 60 / 24  # 15 minutes in days
        end_time = arr.shape[1] * timestep
        time_col = np.arange(0, end_time, timestep)
        out = np.insert(out, 0, time_col, axis=2)
        return out
