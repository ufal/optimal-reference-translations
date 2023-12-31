
import copy
import random


def select_subset(S, B, quality_lambda, temp=1):
    import numpy as np
    assert type(S) is set

    S = copy.deepcopy(S)

    def sigmoid(z):
        return 1/(1 + np.exp(-z))

    def cost_l(l):
        return {
            1: 1,
            2: 1,
            3: 2,
            4: 3,
        }[l]

    def utility_l(l):
        return {
            1: 1,
            2: 2,
            3: 4,
            4: 3,
        }[l]

    def cost(R):
        return sum(
            cost_l(l) * len(R_v)
            for l, R_v in R.items()
        )

    def prob_pos(l):
        return sigmoid(+utility_l(l)-cost_l(l))**(1/temp)

    def prob_neg(l):
        return sigmoid(-utility_l(l)+cost_l(l))**(1/temp)

    R = {
        1: S,
        2: set(),
        3: set(),
        4: set(),
    }

    out = copy.deepcopy(R)
    try:
        while cost(R) < B:
            out = copy.deepcopy(R)
            operation = random.choices(
                population=["REPLACE", "ADD"],
                weights=[quality_lambda, 1-quality_lambda],
                k=1
            )[0]
            candidates_new = [
                (x, l)
                for l in R.keys()
                # what could be added to R[i]?
                for x in S-R[l]
            ]
            candidates_old = [
                (x, l)
                for l in R.keys()
                # what could be removed from R[i]?
                for x in R[l]
            ]
            
            if operation == "REPLACE":
                candidate_old = random.choices(
                    population=candidates_old,
                    weights=[prob_neg(x[1]) for x in candidates_old],
                    k=1,
                )[0]

                # filter candidates to have a higher utility and be the same segment but from a different vendor
                candidates_new = [
                    x for x in candidates_new
                    if utility_l(x[1]) > utility_l(candidate_old[1]) and x[0] == candidate_old[0] and x[1] != candidate_old[1]
                ]

                candidate_new = random.choices(
                    population=candidates_new,
                    weights=[prob_pos(x[1]) for x in candidates_new],
                    k=1,
                )[0]
                
                # commit transaction
                R[candidate_new[1]].add(candidate_new[0])
                R[candidate_old[1]].remove(candidate_old[0])

            elif operation == "ADD":
                candidate_new = random.choices(
                    population=candidates_new,
                    weights=[prob_pos(x[1]) for x in candidates_new],
                    k=1,
                )[0]

                # commit transaction
                R[candidate_new[1]].add(candidate_new[0])
            else:
                raise Exception("Unknown operation")
    except:
        # break when operation fails to be applied
        pass

    return out

def select_subset_old(S, B, quality_lambda, temp=1):
    """
    WARNING: This is the old version without softmax for probability.
    """
    assert type(S) is set

    S = copy.deepcopy(S)

    def cost(R):
        return 1*len(R[1])+1.5*len(R[2])+2*len(R[3])+2.5*len(R[4])

    def utility(i):
        return {
            1: 1/1,
            2: 2/1,
            3: 3/2,
            4: 2/3,
        }[i]

    R = {
        1: S,
        2: set(),
        3: set(),
        4: set(),
    }

    out = copy.deepcopy(R)
    while cost(R) < B:
        out = copy.deepcopy(R)
        operation = random.choices(
            population=["REPLACE", "ADD"],
            weights=[quality_lambda, 1-quality_lambda],
            k=1
        )[0]
        candidates_new = [
            (x, i, utility(i))
            for i in R.keys()
            # what could be added to R[i]?
            for x in S-R[i]
        ]
        candidates_old = [
            (x, i, utility(i))
            for i in R.keys()
            # what could be removed from R[i]?
            for x in R[i]
        ]

        if not candidates_new or not candidates_old:
            break
        
        patience = 0
        if operation == "REPLACE":
            candidate_old = random.choices(
                population=candidates_old,
                weights=[x[2]**(-1/temp) for x in candidates_old],
                k=1,
            )[0]

            # filter candidates to have a higher utility and be the same segment but from a different vendor
            candidates_new = [
                x for x in candidates_new
                if x[2] >= candidate_old[2] and x[0] == candidate_old[0] and x[1] != candidate_old[1]
            ]

            if not candidates_new:
                patience += 1
                if patience >= 10:
                    break
                continue
            else:
                patience = 0

            candidate_new = random.choices(
                population=candidates_new,
                weights=[x[2]**(1/temp) for x in candidates_new],
                k=1,
            )[0]
            
            # commit transaction
            R[candidate_new[1]].add(candidate_new[0])
            R[candidate_old[1]].remove(candidate_old[0])

        elif operation == "ADD":
            candidate_new = random.choices(
                population=candidates_new,
                weights=[x[2]**(1/temp) for x in candidates_new],
                k=1,
            )[0]

            # commit transaction
            R[candidate_new[1]].add(candidate_new[0])
        else:
            raise Exception("Unknown operation")

    return out