import argparse
from itertools import combinations, permutations, product
from os.path import basename


def cycles(n):
    # cycles in a complete graph with n nodes
    return [[c[0]] + list(p) for h in range(1, n+1)
                             for c in combinations(range(n), h)
                             for p in permutations(c[1:])]


def label(f, p, i, j):
    return (f[tuple(p[i] if i!=j else 0 for i in range(len(p)))][i],
            f[tuple(p[i] if i!=j else 1 for i in range(len(p)))][i])


def labels(f, p, c):
    return [label(f, p, i, j) for i, j in zip(c, c[1:] + [c[0]])]


def neighbours(x):
    return [tuple([x[j] if j!=i else 1-x[j] for j in range(len(x))])
            for i in range(len(x))]


def paths_max_steps(x, k):
    # return paths from x of length up to k
    p = {0: [[x]]}
    for l in range(1, k+1):
        paths = []
        for path in p[l-1]:
            ns = neighbours(path[-1])
            for neigh in ns:
                if neigh not in path:
                    paths.append(path + [neigh])
        p[l] = paths
    # k=0 not necessary since we impose f1(0,...,0)=1
    return [path for i in range(1, k+1) for path in p[i]]


def formula(n, k, fixed_points=False):
    # states: {0, 1}^n
    states = sorted(list(product(*[(0, 1)]*n)))
    # variables: 1,2,3,...,n for f(0,0,...,0), n+1,...,2n for f(0,...,0,1), etc
    f = {states[i]: [n*i+j+1 for j in range(n)] for i in range(len(states))}
    form = []

    if fixed_points:
        for x in states:
            form.append([-f[x][i] if x[i] else f[x][i] for i in range(n)])
    else:
        # Condition k for (0,...,0)
        for path in paths_max_steps((0,)*n, k):
            cs = []
            for i in range(len(path)-1):
                ind = [j for j in range(n) if path[i][j]!=path[i+1][j]][0]
                cs.append(-f[path[i]][ind] if path[i+1][ind] else f[path[i]][ind])
            x = path[-1]
            form.append(cs + [-f[x][i] if x[i] else f[x][i] for i in range(n)])

    # no local negative circuits
    circuits = cycles(n)
    for p in states:
        for c in circuits:
            labs = labels(f, p, c)
            k = len(labs)
            for m in range(1, k+1, 2):
                for ls in combinations(labs, m):
                    lsc = [l for l in labs if l not in ls]
                    form.append([l[1] for l in ls] + [-l[0] for l in ls] +
                                [-l[1] for l in lsc] + [l[0] for l in lsc])

    # first component of f(0,...,0) is 1
    form.append([1])
    return form


def write_cnf(n, k, filename, fixed_points=False):
    nvars = n*2**n
    form = formula(n, k, fixed_points)
    with open(filename, "w") as f:
        f.write("c " + basename(filename) + "\n")
        f.write("c\n")
        f.write("p cnf " + str(nvars) + " " + str(len(form)) + "\n")
        for orclause in form:
            f.write(" ".join(map(str, orclause)) + " 0\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="number of variables (default is 2)", default=2)
    parser.add_argument("-k", type=int, help="max path length (default is 2)", default=2)
    parser.add_argument("-fixed", action="store_true", help="write formula for no fixed points")
    parser.add_argument("-file", type=str, help="path to file (default is cnf_files/N_K.cnf or cnf_files/N_nfp.cnf)")
    args = parser.parse_args()

    n, k = args.n, args.k

    filename = args.file
    if not filename:
        if args.fixed:
            filename = "cnf_files/{}_nfp.cnf".format(n)
        else:
            filename = "cnf_files/{}_{}.cnf".format(n, k)

    write_cnf(n, k, filename, args.fixed)
