import random
import math
from os import system, name
import matplotlib.pyplot as plt


#editable
max_populasi = 20
length_gen = 12
mutation_rate = 0.2
crossover_rate = 1
max_evolution = -1 # gunakan -1 evolusi tanpa batas (mencari sampai semua nilai individu konstan) / gunakan batasan tertentu hingga N-Evolusi
parent_sample = 3


lower_x = -5
upper_x = 5

lower_y = -5
upper_y = 5



looping_condition = True
populasi = []
generasi = 1

def clear():
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
       _ = system('clear')

def h(x, y):
  return ((math.cos(x) + math.sin(y)) ** 2) / (x**2) + (y**2)

def f(x, y):
  #fungsi untuk minimasi
  a = random.uniform(0, 0.00000000000000009)
  return 1 / (h(x,y) + a)

def biner_decoding(upper_range, lower_range, g):
    tp = [2**-i for i in range(1, len(g) + 1)]
    #print(tp)
    return lower_range + ((upper_range-lower_range) / sum(tp) * sum([g[i] * tp[i] for i in range(len(g))]))

def generate_cromosome(length):
  bitX = random.choices([0,1], k=length)
  bitY = random.choices([0,1], k=length)
  fenotipeX = biner_decoding(upper_x, lower_x, bitX) #(-5 - 5)
  fenotipeY = biner_decoding(upper_y, lower_y, bitY)

  fitness = f(fenotipeX, fenotipeY)
  return {
    "genX" : bitX,
    "fenX" : fenotipeX,
    "genY" : bitY,
    "fenY" : fenotipeY,
    "cromosome" : bitX + bitY,
    "fitness": fitness
  }

def parent_selection(populasi, parent_sample):
  sample1 = random.choices(populasi, k=parent_sample)
  sample1.sort(key=sortFitness, reverse=True)

  sample2 = random.choices(populasi, k=parent_sample)
  sample2.sort(key=sortFitness, reverse=True)
  return sample1[0], sample2[0]


def crossover(parent1, parent2):
  point = random.randint(1, 2*length_gen-1)
  bit_child1 = parent2["cromosome"][:point] + parent1["cromosome"][point:]
  bit_child2 = parent2["cromosome"][:point] + parent1["cromosome"][point:]

  child1 = dict(parent1)
  child2 = dict(parent2)

  len_genotipe = len(bit_child1)//2
  child1["genX"] = bit_child1[:len_genotipe]
  child1["fenX"] = biner_decoding(upper_x, lower_x, child1["genX"])
  child1["genY"] = bit_child1[len_genotipe:]
  child1["fenY"] = biner_decoding(upper_y, lower_y, child1["genY"])
  child1["cromosome"] = child1["genX"] + child1["genY"]
  child1["fitness"] = f(child1["fenX"], child1["fenY"])


  child2["genX"] = bit_child2[:len_genotipe]
  child2["fenX"] = biner_decoding(upper_x, lower_x, child2["genX"])
  child2["genY"] = bit_child2[len_genotipe:]
  child2["fenY"] = biner_decoding(upper_y, lower_y, child2["genY"])
  child2["cromosome"] = child2["genX"] + child2["genY"]
  child2["fitness"] = f(child2["fenX"], child2["fenY"])



  return child1, child2


def mutation(child, mutation_rate):
  offspring = dict(child)
  offspring["cromosome"] = list(child["cromosome"])
  for i in range(len(offspring["cromosome"])):
    if random.uniform(0,1) <= mutation_rate:
      if offspring["cromosome"][i] == 0:
        offspring["cromosome"][i] = 1
      else:
        offspring["cromosome"][i] = 0
  len_genotipe = len(offspring["cromosome"]) // 2
  offspring["genX"] = offspring["cromosome"][:len_genotipe]
  offspring["genY"] = offspring["cromosome"][len_genotipe:]

  offspring["fenX"] = biner_decoding(upper_x, lower_x, offspring["genX"])
  offspring["fenY"] = biner_decoding(upper_y, lower_y, offspring["genY"] )

  offspring["fitness"] = f(offspring["fenX"], offspring["fenY"])

  return offspring


def create_population(pop):
  while len(populasi) < pop:
    #memasukan sujumlah max_populasi sebagai ruang sample
    populasi.append(generate_cromosome(length_gen))
  
  #melakukan sorting untuk mengambil 2 terbaik  
  populasi.sort(key=sortFitness, reverse=True)
  return populasi

def evaluation(population, generasi):
  if len(population) > 0 and max_evolution == -1:
    return all(round(x["fitness"]) == round(population[0]["fitness"]) for x in population)
  elif max_evolution <= generasi:
    return True
  else:
    return False
    
def sortFitness(e):
  return e['fitness']

def logging(population, generation):
  clear()
  print("Generasi      :", generation)
  print("Best Fitness  :", population[0]["fitness"]/(10**4), "x 10^4")
  print("Best X        :", population[0]["fenX"])
  print("Best Y        :", population[0]["fenY"])
  print("Cromosome     :", population[0]["cromosome"])




def regeneration(children, populasi):
  for i in children:
    if i["fitness"] >= populasi[-1]["fitness"]:
      populasi[-1] = i
    populasi.sort(key=sortFitness, reverse=True)
  return populasi

populasi = create_population(max_populasi)
x = []
y = []

while looping_condition:
  #evaluation
  looping_condition = not evaluation(populasi, generasi)
  logging(populasi, generasi)
  #selection parent
  parent1, parent2 = parent_selection(populasi, parent_sample)
  
  if random.uniform(0,1) <= crossover_rate:
    child1, child2 = crossover(parent1, parent2)
    mutant1 = mutation(child1, mutation_rate)
    mutant2 = mutation(child2, mutation_rate)
    children = [mutant1, mutant2]
  else:
    children = [parent1, parent2]

  populasi = regeneration(children,populasi)
  x.append(generasi)
  y.append(populasi[0]["fitness"])
  generasi += 1

fig, ax = plt.subplots()
ax.plot(x, y)
plt.title('Grafik Evolusi')
plt.xlabel('Generasi')
plt.ylabel('Fitness') 
plt.show()




