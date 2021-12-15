---
description: Создание чекпоинтов в эволюционном обучении в DEAP
tags: ml
---
# Deap чекпоинты

[Статья](https://deap.readthedocs.io/en/master/tutorials/advanced/checkpoint.html)

Суть в следующем: если используется стандартный алгоритм, например `eaSimple`, то необходимо сделат ьего копию и переписать, добавив сериализацию данных. Нужно получить все объекты обучения на (в примере это делается на заданном шаге обучения) и сохранить в объекте `pickle`. При запуске следующего раунда обучения можно полностью восстановить обучающие параметры, включая фенотипы генов и продолжить обучение с той же точки, на которой произошла остановка.

Полностью пример

```python
import pickle

def main(checkpoint=None):
    if checkpoint:
        # A file name has been given, then load the data from the file
        with open(checkpoint, "r") as cp_file:
            cp = pickle.load(cp_file)
        population = cp["population"]
        start_gen = cp["generation"]
        halloffame = cp["halloffame"]
        logbook = cp["logbook"]
        random.setstate(cp["rndstate"])
    else:
        # Start a new evolution
        population = toolbox.population(n=300)
        start_gen = 0
        halloffame = tools.HallOfFame(maxsize=1)
        logbook = tools.Logbook()

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("max", numpy.max)

    for gen in range(start_gen, NGEN):
        population = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        halloffame.update(population)
        record = stats.compile(population)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)

        population = toolbox.select(population, k=len(population))

        if gen % FREQ == 0:
            # Fill the dictionary using the dict(key=value[, ...]) constructor
            cp = dict(population=population, generation=gen, halloffame=halloffame,
                      logbook=logbook, rndstate=random.getstate())

            with open("checkpoint_name.pkl", "wb") as cp_file:
                pickle.dump(cp, cp_file)
```

- [[deap]]
- [[deap-docs]]
- [[deap-multicor-usage]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[deap]: deap "Deap - генетические алгоритмы на python"
[deap-docs]: deap-docs "Deap документация"
[deap-multicor-usage]: deap-multicor-usage "Multicor for "
[//end]: # "Autogenerated link references"