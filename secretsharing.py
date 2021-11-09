import random
from decimal import Decimal

FIELD_SIZE = 10 ** 3


def reconstruct_secret(shares):
    sums = 0
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi) / (xi - xj))
        prod *= yj
        sums += Decimal(prod)
    return int(round(Decimal(sums), 0))


def polynom(x, coefficients):
    point = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def coeff(t, secret):
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff


def generate_shares(n, m, secret):
    coefficients = coeff(m, secret)
    shares = []
    for i in range(1, n + 1):
        x = i
        shares.append((x, polynom(x, coefficients)))
    return shares


num = int(input("Enter the total number of shares : "))
threshold = int(input("Enter the threshold number of shares required to reconstruct the key : "))
shares = generate_shares(num, threshold, 2)
print(shares)

t = int(input('Enter the number of shares you have :'))
shares = []
for i in range(t):
    ind = int(input("Enter the index number of the share : "))
    val = int(input("Enter the value of the share : "))
    shares.append((ind, val))
print(reconstruct_secret(shares))

# print(generate_shares(5, 3, 2))

# # Driver code
# if __name__ == '__main__':
#     # (3,5) sharing scheme
#     t, n = 3, 5
#     secret = 2
#     print(f'Original Secret: {secret}')
#
#     # Phase I: Generation of shares
#     shares = generate_shares(n, t, secret)
#     print(f'Shares: {", ".join(str(share) for share in shares)}')
#
#     # Phase II: Secret Reconstruction
#     # Picking t shares randomly for
#     # reconstruction
#     pool = random.sample(shares, t)
#     print(f'Combining shares: {", ".join(str(share) for share in pool)}')
#     print(f'Reconstructed secret: {reconstruct_secret(pool)}')
