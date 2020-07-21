class UF:

    def __init__(self, N):
        self.N = N
        self.count = N
        self.elements = [ i for i in range(N) ]

    def find(self, p):
        while p != self.elements[p]:
            p = self.elements[p]
        return p
    
    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        root_p = self.find(p)
        root_q = self.find(q)
        if root_p == root_q: return

        self.elements[root_p] = root_q
        self.count -= 1

    

    