def bad_function():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):
                    for m in range(10):
                        for n in range(10):
                            for o in range(10):
                                print(i, j, k, l, m, n, o)


def another_bad():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):
                    print(i, j, k, l)
                    print(i, j, kl)
