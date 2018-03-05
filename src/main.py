from grid import Grid


grids = [
    # 'a_example.in',
    # 'b_should_be_easy.in',
    'c_no_hurry.in',
    # 'd_metropolis.in',
    # 'e_high_bonus.in'
]


best_score = 0

while True:
    total_score = 0

    for i in grids:

        with open('../inputs/%s' % i) as f:
            g = Grid()
            g.read(f)

        g.solve_randomized_greedy()

        if g.total_score() > best_score:
            with open('../outputs/%s#score=%d.txt' % (i, g.total_score()), 'w') as f:
                g.write(f)
            best_score = g.total_score()

        print('%s done! Score: %d' % (i, g.total_score()))
        total_score += g.total_score()

    print('Total Score:%d' % total_score)
