from collections import deque

class Sim:
    def __init__(self, rs, ns, nd, mw, srt, drt):
        self.r = rs
        self.v = set('AEIOU')
        self.l = deque(rs)
        self.ws = {r: 0 for r in rs if r[0] in self.v}
        self.ns = ns
        self.nd = nd
        self.srt = srt
        self.drt = drt
        self.avs = ns
        self.avd = nd
        self.r = []

    def is_vr(self, r):
        return r[0] in self.v

    def sim_turn(self):
        assigned = False
        tl = list(self.l)
        i = 0
        while i < len(tl) and not assigned:
            r = tl[i]
            if self.avd > 0:
                self.avd -= 1
                rsd = [self.l.popleft()]
                if self.l:
                    rsd.append(self.l.popleft())
                self.r.append(('d', self.drt, rsd))
                assigned = True
            elif self.avs > 0:
                if self.is_vr(r) and self.ws.get(r, 0) < 2:
                    self.ws[r] += 1
                    i += 1
                else:
                    self.avs -= 1
                    self.l.popleft()
                    self.r.append(('s', self.srt, [r]))
                    assigned = True
            else:
                break

        for i in range(len(self.r) - 1, -1, -1):
            tube_type, tm, rs_list = self.r[i]
            self.r[i] = (tube_type, tm - 1, rs_list)
            if self.r[i][1] <= 0:
                for r in rs_list:
                    self.l.append(r)
                    if r in self.ws:
                        self.ws[r] = 0
                del self.r[i]
                if tube_type == 's':
                    self.avs += 1
                else:
                    self.avd += 1

    def display_status(self, turn):
        print(f"Turn {turn}:")
        print(f"  Line: {list(self.l)}")
        print(f"  Riders: {[(t, tl, r) for t, tl, r in self.r]}")
        print("-" * 40)

    def run_sim(self, num_turns):
        for turn in range(1, num_turns + 1):
            self.sim_turn()
            self.display_status(turn)

def main():
    rs = list("ABCDEFGHIJKLMNOPQRSTUV")
    ns = 5
    nd = 1
    srt = 5
    drt = 4

    sim = Sim(rs, ns, nd, 2, srt, drt)
    sim.run_sim(20)

