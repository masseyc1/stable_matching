Basic implementation of [Gale-Shapley](https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm) algorithm for computing stable matchings between ``doctors'' and ``hospitals''.

Implements the doctor-proposing variant of Gale-shapley, which yields the doctor-optimal stable matching (in the sense that the
resulting stable matching lies at the top of the [stable-matching lattice](https://en.wikipedia.org/wiki/Lattice_of_stable_matchings))
