#!/usr/bin/env python
"""
Calculates rmax for LOCI acccording to
Papadimitriou, Spiros, et al.
"Loci: Fast outlier detection using the local correlation integral."
Data Engineering,
2003. Proceedings. 19th International Conference on. IEEE, 2003.

Returns rmax

Usage: locirmax [OPTION] FILE ALPHA
Options:
--header  Tells the script that the FILE has a string header

"""
import math
import sys


def print_msg(msg):
  print("[locirmax] "+str(msg))

def main(args):
  if len(args) < 1:
    print_msg("Argument FILE missing!")
    sys.exit(1)

  if len(args) < 2:
    print_msg("Argument ALPHA missing!")
    sys.exit(1)

  header = False
  arg_offset = 0

  if args[0] == "--header":
    header = True
    arg_offset = arg_offset + 1

  file_path = args[arg_offset]
  alpha = float(args[arg_offset + 1])

  csv_file = open(file_path, 'r')
  points = csv_file.readlines()
  dists = list()
  p_len = len(points)

  for i in range(0, p_len):
    if header and i == 0:
      continue
    for j in range(0, p_len):
      if j <= i:
        continue
      if header and j == 0:
        print_msg("j is header")
        continue
      dists.append(euclidean_dist(points[i], points[j]))

  csv_file.close()
  rmax = pow(alpha, -1) * max(dists)
  print_msg("Calculated rmax: "+str(rmax))
  return rmax


def euclidean_dist(point_a, point_b):
  """
  Calculates the euclidean distance between two points.
  """
  point_a = point_a.split(",")
  point_b = point_b.split(",")

  if len(point_a) != len(point_b):
    print_msg("The points are of different dimensions!")
    print_msg(len(point_a))
    print_msg(len(point_b))
    sys.exit(1)

  dsum = 0
  for index, point_a_i in enumerate(point_a):
    try:
      val = float(point_a[index]) - float(point_b[index])
    except ValueError:
      print_msg("Data contains non-numerical data!")
      print_msg("point_a: "+str(point_a[index]))
      print_msg("point_b: "+str(point_b[index]))
      print_msg("Aborting!")
      sys.exit(1)
    val = pow(val, 2)
    dsum = dsum + val

  return math.sqrt(dsum)

if __name__ == "__main__":
  main(sys.argv[1:])
