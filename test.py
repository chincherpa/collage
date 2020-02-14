cols = 3
rows = 3


def get_optimal_space(w, h, ratio):
  print(f"{w=}, {h=}, {ratio=}")
  res = []
  for x in range(100):
      x_term = x + (w + x) * cols
      dc = h * rows
      space_y = ((x_term / ratio) - dc) / (rows + 1)
      if space_y.is_integer() and space_y > 0:
          res.append((x, space_y))
  print(*res, sep="\n")
  print("#" * 30)


get_optimal_space(200, 300, 1)
