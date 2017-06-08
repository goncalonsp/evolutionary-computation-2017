#Self-Adaptation in Evolutionary Strategies
##Evolutionary Computation Project

Function used for plotting the mathematical functions based on one implementation found in:
https://stackoverflow.com/questions/8722735/i-want-to-use-matplotlib-to-make-a-3d-plot-given-a-z-function

# How to run:

The `standard.py` is the implementation of the Standard approach and the `self_adaptation.py` is the self adaptive one. Each takes one configuration file with the problem and evolutionary algorithm parameters, `conf_standard.json` and `conf_adaptation.json` respectively.

To run one time and plot results:

    ```
        $ python standard.py -c conf_standard.json
        $ python self_adaptation.py -c conf_adaptation.json
    ```

To run multiple times and plot results:

    ```
        $ python standard.py -r 30 -c conf_standard.json
        $ python self_adaptation.py -r 30 -c conf_adaptation.json
    ```

To run multiple times and output to `*.stats` files the best fitness on each run (used for the report):

    ```
        $ python standard.py -t -r 30 -c conf_standard.json
        $ python self_adaptation.py -t -r 30 -c conf_adaptation.json
    ```

To run the experiments used in the report with the exact same values:

    ```
        $ python standard.py -t -r 30 -c experiments/rastrigin/conf_standard.json
        $ python self_adaptation.py -t -r 30 -c experiments/rastrigin/conf_adaptation.json

        $ python standard.py -t -r 30 -c experiments/schwefel/conf_standard.json
        $ python self_adaptation.py -t -r 30 -c experiments/schwefel/conf_adaptation.json

        $ python standard.py -t -r 30 -c experiments/dejong1/conf_standard.json
        $ python self_adaptation.py -t -r 30 -c experiments/dejong1/conf_adaptation.json

        $ python standard.py -t -r 30 -c experiments/griewangk/conf_standard.json
        $ python self_adaptation.py -t -r 30 -c experiments/griewangk/conf_adaptation.json
    ```

To analyse the results as reported in the report:

    ```
        $ python stat_this.py experiments/rastrigin
        $ python stat_this.py experiments/schwefel
        $ python stat_this.py experiments/dejong1
        $ python stat_this.py experiments/griewangk
    ```

## Configuration files

Example of configuration for the Standard algorithm:

    ```
        {
            "problem_function": "rastrigin_eval",
            "dimensionality": 20,
            "domain": [-5.12, 5.12],

            "number_generations": 1000,
            "size_population": 100,

            "mutation": {
                "probability": 0.01,
                "function": "muta_float_gaussian",
                "sigma": 0.5
            },
            "crossover": {
                "probability": 0.9,
                "alpha": 0.3,
                "function": "heuristical_cross"
            },

            "tournament_size": 5,
            "elite_percentage": 0.1
        }
    ```

And for the Adaptive algorithm:

    ```
        {
            "problem_function": "rastrigin_eval",
            "dimensionality": 20,
            "domain": [-5.12, 5.12],

            "number_generations": 1000,
            "size_population": 100,

            "mutation": {
                "probability": 0.01,
                "function": "muta_float_gaussian",
                "sigma_domain": [0, 1]
            },
            "crossover": {
                "probability": 0.9,
                "alpha": 0.3,
                "function": "heuristical_cross"
            },

            "tournament_size": 5,
            "elite_percentage": 0.1
        }
    ```