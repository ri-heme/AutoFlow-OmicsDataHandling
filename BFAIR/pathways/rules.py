"""Rules.

This module contains functions to apply reaction rules to chemical compounds.
"""

from functools import reduce

import numpy as np
import pandas as pd

from cobra.core.singleton import Singleton


class RuleLibrary(metaclass=Singleton):

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self.reset()

    def __iter__(self):
        return self.available_rules.itertuples(index=False, name=None)

    def __len__(self):
        return len(self.available_rules)

    def __repr__(self):
        return repr(self.available_rules)

    @property
    def available_rules(self):
        if self._filters:
            return self._data[reduce(np.logical_and, self._filters)]
        else:
            return self._data

    def apply_to(self, input_compound, input_type):
        """
        Applies the available rules to the input compound.

        Parameters
        ----------
        input_compound : str
            String representation of a chemical compound.
        input_type : {'inchi', 'smiles'}
            Type of notation describing the input compound.

        Returns
        -------
        list
            List of rule IDs and resulting products from reactions.
        """
        raise NotImplementedError()

    def filter_by_metanetx_id(self, *args):
        """
        Applies a filter to the rule library that excludes reactions that do not match the given MNXref identifiers.
        """
        raise NotImplementedError()

    def filter_by_organism(self, model_name, additional_identifiers=None):
        """
        Applies a filter to the rule library that excludes reactions that are not available in the input genome-scale
        model.
        """
        raise NotImplementedError()

    def filter_by_compound(self, input_compound, input_type, bio_score_cutoff=0.1, chem_score_cutoff=0.7):
        """
        Returns a set of reaction rules from the input library that can be applied to input compound, based on
        biochemical uncertainty and chemical similarity.

        Parameters
        ----------
        input_compound : str
            String representation of a compound.
        input_type : {'inchi', 'smiles'}
            Type of notation describing the input compound.
        bio_score_cutoff : float
            Biochemical uncertainty score below which reaction rules are filtered out. Each reaction rules has an
            associated score that functions as a proxy for uncertainty and specificity. Scores closer to 0 indicate less
            uncertainty and higher specificity with respect to the annotated enzyme sequences. Note that, due to how it
            is calculated, the score is biased against rarely studied enzymes.
        chem_score_cutoff : float
            Chemical similarity score (between the input compound and the native substrate of a reaction) below which a
            reaction rule is considered inapplicable. The chemical similarity score between two compounds ranges from 0
            to 1, the latter meaning both molecules are identical.
        """
        raise NotImplementedError()

    def pop_filter(self, index=-1):
        """
        Removes the filter at the given index from the list of filters.

        Parameters
        ----------
        index : int
            Index of filter to be popped.
        """
        self._filters.pop()

    def reset(self):
        """
        Resets the applied filters.
        """
        self._filters = []
