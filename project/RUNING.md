# Running the various scripts

# TTP combined (LinKern, TSP EA and KP heuristic)

For the TTP combined the `ttp.py` file is used. The following reads the configuration in file `config_perm.json` and instance file. The instance file is the only mandatory parameter, however if no configuration file is provided defaults set in the code will be used.

```
    $ python ttp.py -c config_perm.json instances/a280_n279_bounded-strongly-corr_01.ttp
```

Equal to above but using a configuration file set to use random key representation in the TSP EA.

```
    $ python ttp.py -c config_randkey.json instances/a280_n279_bounded-strongly-corr_01.ttp
```

## Configuration

* `use_linkern` setting controls if the TSP tours are directly read from the * file or not. In the negative case the TSP EA is run.
* `top_k` setting controls the number of best tours returned by the TSP EA.
* `development` setting under `tsp` controls if the algorithm is run multiple times or just one. The number of runs is specified by `runs`.
* `plot_generations` setting can be set to true to display plots;
* `representation` can be set to `random key` or `permutation` to change the TSP EA representation;
* `gen_population` setting can be set to `heuristic`, `random` or `dist_heuristic`. This controls the TSP EA's initial population generation.

All other parameters control other common settings of a EA algorithm and are self explanatory.

```
    {
        "use_linkern": false,
        "top_k": 5,
        "tsp": {
            "development": true,
            "plot_generations": true,
            "runs": 5,
            "fitness": "distance",
            "interpretation": "simple",
            "representation": "permutation",
            "mutation": {
                "probability": 0.02,
                "sigma": 0.1
            },
            "crossover": {
                "probability": 0.8
            },
            "tournament_size": 5,
            "elite_percentage": 0.1,
            "number_generations": 1000,
            "size_population": 100,
            "maximum_chromosome_size": 100,
            "gen_population": "random" 
        }
    }
```

# TTP EA

For the TTP EA the `ttp_ea.py` is used. The following reads the configuration in file `config_ttp_ea.json`, runs the EA for 30 runs and outputs the plot of the fitness over runs to file `plot.png`. The instance file is only mandatory parameter, however if no configuration file is provided defaults set in the code will be used.

``` 
    $ python ttp_ea.py -c config_ttp_ea.json -r 30 -s plot.png instances/a280_n279_bounded-strongly-corr_01.ttp
```

Next one, reads the configuration in file `config_ttp_ea.json`, runs the EA one time and outputs the plot of the fitness over generations to file `plot.png`.

```
    $ python ttp_ea.py -c config_ttp_ea.json -s plot.png instances/a280_n279_bounded-strongly-corr_01.ttp
```

Next one, reads the configuration in file `config_ttp_ea.json`, runs the EA one time.

```
    $ python ttp_ea.py -c config_ttp_ea.json instances/a280_n279_bounded-strongly-corr_01.ttp
```

## Configuration

* `plot_generations` setting can be set to true to display plots;
* `initial_pop` setting can be set to `heuristic`, `random`. This controls the TSP EA's initial population generation.

All other parameters control other common settings of a EA algorithm and are self explanatory.

```
    {
        "plot_generations": false,
        "tsp": {
            "mutation": {
                "probability": 0.01
            },
            "crossover": {
                "probability": 0.7
            },
            "initial_pop": "heuristic"
        },
        "kp": {
            "mutation": {
                "probability": 0.01
            },
            "crossover": {
                "probability": 0.8
            }
        },
        "tournament_size": 5,
        "elite_percentage": 0.1,
        "number_generations": 100,
        "size_population": 100
    }
```

# KP EA

The following runs the KP EA on the provided instance and by reading the configuration file `config_kp.json`. The instance file is the only mandatory parameter, however if no configuration file is provided defaults set in the code will be used.

```
    $ python kp.py -c config_kp.json instances/a280_n279_bounded-strongly-corr_01.ttp
```

## Configuration

* `development` setting controls if the algorithm is run multiple times or just one. The number of runs is specified by `runs`.
* `plot_generations` setting can be set to true to display plots;

All other parameters control other common settings of a EA algorithm and are self explanatory.

```
    {
        "development": false,
        "plot_generations": true,
        "runs": 30,
        "mutation": {
            "probability": 0.01
        },
        "crossover": {
            "probability": 0.8
        },
        "tournament_size": 5,
        "elite_percentage": 0.1,
        "number_generations": 100,
        "size_population": 100
    }
```