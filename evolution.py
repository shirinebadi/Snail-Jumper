import copy
from operator import attrgetter
import os

import numpy as np

from player import Player


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        players.sort(key=lambda x: x.fitness, reverse=True)
        
        # TODO (Additional: Implement roulette wheel here)

        players = self.roulette_wheel(players, num_players)
        self.save_fitness(players)
        # TODO (Additional: Implement SUS here)
        # TODO (Additional: Learning curve)
        return players[: num_players]

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )
            prev_players = [p for p in self.q_tournament(prev_players ,num_players ,3)]
            new_players = self.crossover(prev_players)  # DELETE THIS AFTER YOUR IMPLEMENTATION

            for child in new_players:
                self.mutate(child)

            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player

    ## TODO: improve all MASMALs
    def crossover(self, prev_players):
        new_players = []
        p_cross = 0

        def concate(p1,p2):
            shape =  p1.shape[0] // 2
            ch1 = np.concatenate((p1[:shape], p2[shape:]), axis=0)
            ch2 = np.concatenate((p2[:shape], p1[shape:]), axis=0)
            return   ch1, ch2

        for i in range(0, len(prev_players), 2):
            ch1 = self.clone_player(prev_players[i])
            ch2 = self.clone_player(prev_players[i+1])

            random_number = np.random.uniform(0, 1, 1)
            if random_number > p_cross:
                for w in range(len(prev_players[i].nn.weights)):
                    ch1.nn.weights[w], ch2.nn.weights[w] = concate(prev_players[i].nn.weights[w], prev_players[i+1].nn.weights[w])

                for w in range(len(prev_players[i].nn.biasis)):
                    ch1.nn.biasis[w], ch2.nn.biasis[w] = concate(prev_players[i].nn.biasis[w], prev_players[i+1].nn.biasis[w])

                new_players.append(ch1)
                new_players.append(ch2)
            else:
                new_players.append(prev_players[i])
                new_players.append(prev_players[i+1])

        return new_players

    def mutate(self, child):
        pw_mutation = 0.82
        pb_mutation = 0.82

        for i in range(len(child.nn.weights)):
            if np.random.random_sample() >= pw_mutation:
                child.nn.weights[i] += np.random.normal(0, 0.14, size=(child.nn.weights[i].shape))

        for i in range(len(child.nn.biasis)):
            if np.random.random_sample() >= pb_mutation:
                child.nn.biasis[i] += np.random.normal(0, 0.14, size=(child.nn.biasis[i].shape))

    def q_tournament(self ,players, num ,k = 3):
        for n in range(num):
            q_selections = np.random.choice(players, k)
            m = (max(q_selections, key=attrgetter('fitness')))
            yield  m

    def roulette_wheel(self, players, n):
        total = sum([player.fitness for player in players])
        prob = [p.fitness/total for p in players] 
        print('total: ', total)
        i = 0
        ##w, v = players[0].fitness, players[0]
        res =  np.random.choice(players, size = n, p=prob, replace=False)
        print(type(res))
        return list(res)


    def save_fitness(self, players):
        try:
            f = open("fitness.txt", "a")
        except FileNotFoundError:
            os.mkdir('fitness.txt')
        for p in players:
            f.write(str(p.fitness))
            f.write(" ")
        f.write("\n")
        f.close()
