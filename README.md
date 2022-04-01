# Fairness with entitlements

This repository contains the experiments that will be described in the following paper:

[Weighted Fairness Notions for Indivisible Items Revisited](https://arxiv.org/abs/2112.04166), by Mithun Chakraborty, Erel Segal-Halevi, Warut Suksompong (2021--2022).

There are four experiments. Each experiment allocates a set of discrete goods among agents with different preferences and different entitlements. The allocation is done uses an algorithm called *divisor picking sequence* with a parameter `y`. After an allocation is found, we check whether it satisfies various fairness notions, which are explained in the paper. Each experiment is devoted to a single fairness notion:

* [Normalized Maximin Share](picking-NMMS.py)
* [Weighted Maximin Share](picking-WMMS.py)
* [Weighted Envy-Freeness](picking-WEF.py)
* [Weighted Proportionality](picking-WPROP.py)
* [Weighted Proportionality](picking-WPROP-numpy.py)
